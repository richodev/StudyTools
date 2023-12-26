from Notion.NotionConnector import NotionConnector
from Notion.NotionCoursePage import NotionCoursePage
from PdfParser.PdfParser import PdfParser

import argparse
import logging
import sys


#----- Logging -----
g_logger = logging.getLogger("Script2Notion")
g_logger.setLevel(logging.DEBUG)

stdFormatter = logging.Formatter("[%(module)s][%(levelname)s] %(message)s")

stdoutHandler = logging.StreamHandler(sys.stdout)
stdoutHandler.setFormatter(stdFormatter)
g_logger.addHandler(stdoutHandler)

fileHandler = logging.FileHandler("ScriptToNotionExtractor.log", mode="w")
fileHandler.setFormatter(stdFormatter)
g_logger.addHandler(fileHandler)


#----- Command Line Parser -----
g_cmdLineParser = argparse.ArgumentParser(
    description="""This command line utility can be used to extract the slides of a lecture script 
    and publish them to a Notion page.""",
    add_help=True)

g_cmdLineParser.add_argument(
    "lectureScriptPath",
    help="The path to the lecture script file (must be a PDF file).",
    type=str)

g_cmdLineParser.add_argument(
    "courseNumber",
    help="""The course number which the lecture belongs to. This number is used to find the Notion 
    course page where the slides will be published to.""",
    type=str)

g_cmdLineParser.add_argument(
    "-t", "--notionToken",
    help="""Specifies the Notion secret token which should be used when accessing the Notion API.""",
    type=str, required=False)

g_cmdLineParser.add_argument(
    "-o", "--overwrite",
    help="""Determines how the lecture script will be published to Notion if a lecture notes page with the 
     same title already exists. If true and there is an existing Notion page with the same name the existing page 
     will be archived and a new site will be created. If false and update is false aswell the script will terminate.""",
    type=bool, default=False, required=False)

g_cmdLineParser.add_argument(
    "-u", "--update",
    help="""Determines how the lecture script will be published to Notion if a lecture notes page with the 
     same title already exists. If true and there is an existing Notion page with the same name the existing page 
     will be updated. If false and overwrite is false aswell the script will terminate.""",
     type=bool, default=False, required=False)

g_cmdLineParser.add_argument(
    "-s", "--skipPublish",
    help="""If set to true the publishing of the lecture script will be skipped.""",
     type=bool, default=True, required=False)


#----- Main -----
def main():
    g_logger.info("Starting script...")
    
    args = g_cmdLineParser.parse_args(sys.argv[1:])
    g_logger.debug(f"Cmd Line Args: {args}")

    pdfParser = PdfParser(args.lectureScriptPath)

    if not args.skipPublish:
        notionConnector = NotionConnector()
        notionCoursePage = NotionCoursePage(args.courseNumber)
        notionCoursePage.PrepareLectureNotesPage("10. Speicherkonsistenz und Synchronisation", args.overwrite, args.update)

    g_logger.info("Script executed.")


if __name__ == "__main__":
    main()