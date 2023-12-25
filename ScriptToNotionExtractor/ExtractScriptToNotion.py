from Notion.NotionConnector import NotionConnector
from Notion.NotionCoursePage import NotionCoursePage

import argparse
import logging
import json
import sys


#----- Logging -----
g_logger = logging.getLogger()
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
    help="The path to the lecture script.",
    type=str)

g_cmdLineParser.add_argument(
    "courseNumber",
    help="""The course number which the lecture belongs to. This number is used to find the Notion 
    course page where the slides will be published to.""",
    type=str)

g_cmdLineParser.add_argument(
    "-o", "--overwrite",
    help="""Determines how the extracted slides will be published to Notion. If false a new Notion page 
    will be created. If true and there is an existing Notion page with the same name the existing page will be 
    overwritten.""",
    type=bool, default=False, required=False)

g_cmdLineParser.add_argument(
    "-u", "--update",
    help="""Determines how the extracted slides will be published to Notion. If false the extracted slides
     will be published to a new Notion page. If true and there is an existing Notion page with the same name the
     existing page will be updated.""",
     type=bool, default=False, required=False)


#----- Main -----
def main():
    g_logger.info("Starting script...")
    
    args = g_cmdLineParser.parse_args(sys.argv[1:])
    g_logger.debug(f"Cmd Line Args: {args}")

    notionConnector = NotionConnector()
    notionCoursePage = NotionCoursePage(args.courseNumber)
    notionCoursePage.PrepareLectureNotesPage("10. Speicherkonsistenz und Synchronisation", args.overwrite, args.update)

    g_logger.info("Script executed.")


if __name__ == "__main__":
    main()