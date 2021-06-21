#!/usr/bin/env python3

import argparse
import requests
import pybtex.database as pybdb
import re

def expand_macros(s : str):
    replacements = {
               "\\_" : "_",
            "\\'{a}" : "á",
            "\\'{e}" : "é",
            "\\'{i}" : "í",
            "\\'{o}" : "ó",
            "\\'{u}" : "ú",
            "\\'{y}" : "ý",
            "\\v{c}" : "č",
            "\\v{s}" : "š",
                 "{" : "",
                 "}" : ""
            }
    for k, r in replacements.items():
        s = s.replace(k, r)
    return s


def format_authors(authors):
    authors_f = ""
    for i in range(len(authors) - 1):
        authors_f += authors[i] + ", "
    authors_f += "and " + authors[-1]
    return authors_f

def read_bibs(args):
    bibs = None
    if args.dblp_id != None:
        dblp_url = "https://dblp.org/pid/{}.bib".format(args.dblp_id)
        bibsponse = requests.get(dblp_url)
        bibs = pybdb.parse_string(bibsponse.text, "bibtex")
    elif args.bibfile != None:
        bibs = pybdb.parse_file(args.bibfile, "bibtex")
    else:
        print("Please specify a DBLP id or a local bibtex file.")
    return bibs

def is_good(year, args):
    if args.since != None and year < args.since:
        return False
    if args.until != None and year > args.until:
        return False
    return True

def has_author(authors, args):
    if args.author != None:
        match_author = args.author.lower()
        return any(match_author in author.lower() for author in authors)
    return True

def main(args):
    bibs = read_bibs(args)
    if bibs != None:
        for bib in bibs.entries:
            thisbib = bibs.entries[bib]
            def get_field(key):
                return expand_macros(thisbib.fields.get(key, ""))

            title = get_field("title")
            authors = list(expand_macros(str(author)) for author in thisbib.persons["author"])

            if not has_author(authors, args):
                continue

            authors_f = format_authors(authors)

            collection = get_field("booktitle") if thisbib.type == "inproceedings" else get_field("journal")
            pages = get_field("pages")
            year = get_field("year")
            if not is_good(year, args):
                continue

            url = None
            if "doi" in thisbib.fields:
                url = "https://doi.org/" + get_field("doi")
            else:
                url = get_field("url")
            url = "\\url{" + url + "}"

            # guess open access status
            
            oa = "Gold OA?"
            publisher = get_field("publisher").lower()
            url_lower = url.lower()
            green_oa = ["springer", "elsevier", "acm"]
            gold_oa = ["arxiv", "eccc", "dagstuhl"]
            if any(pubstring in publisher for pubstring in green_oa):
                oa = "Green OA"
            elif any(venue in url for venue in gold_oa) or "dagstuhl" in publisher:
                oa = "Gold OA"

            print(f"\\tofill{{ {authors_f}: {title}. {collection}, {year}, {pages}, {url}, {oa} }}\\\\\n\\msep")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("dblp_id", metavar="DBLP-id", nargs="?", help="your DBLP id (usually of the form xxx/yyyy or similar)")
    parser.add_argument("-b", "--bibfile", help="parse a local .bib file instead of DBLP")
    parser.add_argument("-u", "--until", help="only return entries up to this year")
    parser.add_argument("-s", "--since", help="only return entries since this year")
    parser.add_argument("-a", "--author", help="only entries with this author")

    args = parser.parse_args()
    main(args)
