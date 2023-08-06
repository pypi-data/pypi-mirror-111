import logging
import re
import fnmatch
from typing import List, Tuple
import os
import os.path
import sys
from subprocess import Popen, PIPE
import shutil
from xml.etree import cElementTree as ET

SOFFICE_PATH = shutil.which("soffice")
JAVA_PATH = shutil.which("java")
RESOURCES_PATH = os.path.dirname(os.path.abspath(__file__)) + "/resources/"
SAXON_PATH = os.getenv("SAXON_PATH") or (RESOURCES_PATH + "saxon9.jar")
XMLLINT_PATH = shutil.which("xmllint")

if not SOFFICE_PATH:
    sys.exit("Could not find soffice. Is it in your PATH ?")
if not JAVA_PATH:
    sys.exit("Could not find java. Is it in your PATH ?")
if not SAXON_PATH:
    sys.exit(
        "Could not find the Saxon jar. Please set SAXON_PATH environment variable."
    )
if not os.path.isfile(SAXON_PATH):
    sys.exit(
        "Could not find the Saxon jar. Please check your SAXON_PATH environment variable."
    )
if not XMLLINT_PATH:
    sys.exit("Could not find xmllint. Is it in your PATH ?")


def _silent_remove(path: str):
    try:
        os.remove(path)
    except FileNotFoundError:
        pass


def _find_files(what: str, where: str = ".") -> List[str]:
    rule = re.compile(fnmatch.translate(what), re.IGNORECASE)
    return [
        "{}{}{}".format(where, os.path.sep, name)
        for name in os.listdir(where)
        if rule.match(name)
    ]


def _process_doc(
    doc_file, working_dir: str, logger: logging.Logger
) -> Tuple[bool, str]:
    doc_file_no_extension = os.path.splitext(doc_file)[0]

    #
    # STEP 1, convert to XML
    #
    p = Popen(
        [
            SOFFICE_PATH,
            "--invisible",
            "--convert-to",
            "xml:OpenDocument Text Flat XML",
            "--outdir",
            working_dir,
            doc_file,
        ],
        stdout=PIPE,
        stderr=PIPE,
    )
    out, err = p.communicate()
    if p.returncode != 0:
        return (
            False,
            err.decode("utf-8") if err else "sub-process provided no error output",
        )
    else:
        logger.info("Wrote {}".format(os.path.basename(doc_file_no_extension + ".xml")))
    p.terminate()

    #
    # STEP 2 : TRANSFORMATIONS XSL
    # 2a, cleanup
    #
    p = Popen(
        [
            JAVA_PATH,
            "-jar",
            SAXON_PATH,
            doc_file_no_extension + ".xml",
            RESOURCES_PATH + "cleanup/cleanup.xsl",
        ],
        stdout=PIPE,
        stderr=PIPE,
    )
    out, err = p.communicate()
    if p.returncode != 0:
        return (
            False,
            err.decode("utf-8") if err else "sub-process provided no error output",
        )
    else:
        with open(doc_file_no_extension + "_01_clean.xml", "wb") as f:
            f.write(out)
            logger.info(
                "Wrote {}".format(
                    os.path.basename(doc_file_no_extension + "_01_clean.xml")
                )
            )

    #
    # STEP 2 : TRANSFORMATIONS XSL
    # 2b, control styles
    #
    p = Popen(
        [
            JAVA_PATH,
            "-jar",
            SAXON_PATH,
            doc_file_no_extension + "_01_clean.xml",
            RESOURCES_PATH + "control/control.xsl",
        ],
        stdout=PIPE,
        stderr=PIPE,
    )
    out, err = p.communicate()
    if p.returncode != 0:
        return (
            False,
            err.decode("utf-8") if err else "sub-process provided no error output",
        )
    else:
        with open(doc_file_no_extension + "_02_control.xml", "wb") as f:
            f.write(out)
            logger.info(
                "Wrote {}".format(
                    os.path.basename(doc_file_no_extension + "_02_control.xml")
                )
            )

    control_xml = ET.fromstring(out.decode("utf-8"))
    for error_node in control_xml.findall(".//FATAL"):
        logger.fatal(error_node.text)
        return False, "Not OK"

    #
    # STEP 2c, hierarchy
    #
    p = Popen(
        [
            JAVA_PATH,
            "-jar",
            SAXON_PATH,
            doc_file_no_extension + "_02_control.xml",
            RESOURCES_PATH + "hierarchize/hierarchize.xsl",
        ],
        stdout=PIPE,
        stderr=PIPE,
    )
    out, err = p.communicate()
    if p.returncode != 0:
        return (
            False,
            err.decode("utf-8") if err else "sub-process provided no error output",
        )
    else:
        with open(doc_file_no_extension + "_03_hierarchize.xml", "wb") as f:
            f.write(out)
            logger.info(
                "Wrote {}".format(
                    os.path.basename(doc_file_no_extension + "_03_hierarchize.xml")
                )
            )

    #
    # STEP 2d, normalisation
    #
    p = Popen(
        [
            JAVA_PATH,
            "-jar",
            SAXON_PATH,
            doc_file_no_extension + "_03_hierarchize.xml",
            RESOURCES_PATH + "normalisation/normalize.xsl",
        ],
        stdout=PIPE,
        stderr=PIPE,
    )
    out, err = p.communicate()
    if p.returncode != 0:
        return (
            False,
            err.decode("utf-8") if err else "sub-process provided no error output",
        )
    else:
        with open(doc_file_no_extension + "_04_normalize.xml", "wb") as f:
            f.write(out)
            logger.info(
                "Wrote {}".format(
                    os.path.basename(doc_file_no_extension + "_04_normalize.xml")
                )
            )

    #
    # STEP 2e, modules
    #
    p = Popen(
        [
            JAVA_PATH,
            "-jar",
            SAXON_PATH,
            doc_file_no_extension + "_04_normalize.xml",
            RESOURCES_PATH + "totei-modules/totei.xsl",
        ],
        stdout=PIPE,
        stderr=PIPE,
    )
    out, err = p.communicate()
    if p.returncode != 0:
        return (
            False,
            err.decode("utf-8") if err else "sub-process provided no error output",
        )
    else:
        with open(doc_file_no_extension + "_05_tei.xml", "wb") as f:
            f.write(out)
            logger.info(
                "Wrote {}".format(
                    os.path.basename(doc_file_no_extension + "_05_tei.xml")
                )
            )
    p.terminate()

    #  _silent_remove(doc_file)
    #  _silent_remove(doc_file_no_extension + ".xml")
    #  _silent_remove(doc_file_no_extension + "_01_clean.xml")

    #
    # STEP 3 : VALIDATION
    #

    p = Popen(
        [
            XMLLINT_PATH,
            "--schema",
            RESOURCES_PATH + "schema/metopes.xsd",
            doc_file_no_extension + "_05_tei.xml",
            "--noout",
        ],
        stdout=PIPE,
        stderr=PIPE,
    )
    out, err = p.communicate()
    if p.returncode != 0:
        logger.error(
            "Validate {} {}".format(
                os.path.basename(doc_file_no_extension + "_05_tei.xml"),
                err.decode("utf-8") if err else "subproces provided no error output",
            )
        )
    else:
        logger.info(
            "Validate {}".format(
                os.path.basename(doc_file_no_extension + "_05_tei.xml validates")
            )
        )

    return True, "All OK"


def doc2tei(working_dir: str, logger: logging.Logger, options: dict = None):
    success_counter = 0
    failure_counter = 0
    doc_files = _find_files("*.docx", working_dir) + _find_files("*.odt", working_dir)
    logger.info("{} file(s) to convert.".format(len(doc_files)))
    for doc_file in doc_files:
        logger.info("converting {}".format(os.path.basename(doc_file)))
        success, output = _process_doc(doc_file, working_dir, logger)
        if not success:
            logger.error("could not convert {}".format(os.path.basename(doc_file)))
            failure_counter = failure_counter + 1
        else:
            success_counter = success_counter + 1
            logger.info("{}: success".format(os.path.basename(doc_file)))
    logger.info("Job done, {} files converted".format(success_counter))


doc2tei.description = {
    "label": "Docx vers TEI",
    "help": "Convertir les fichiers *.docx et *.odt en fichiers *.xml (vocabulaire TEI)",
    "options": [],
}
