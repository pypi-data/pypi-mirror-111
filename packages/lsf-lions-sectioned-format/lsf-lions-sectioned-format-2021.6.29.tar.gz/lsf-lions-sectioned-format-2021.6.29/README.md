# lsf

LSF (Lion's Sectioned Format) is a plain-text container format.

It features:
* header & content sections
* titles for all sections (except the header)
* key-value pairs for all sections (optionally)
* body text for each section (optionally)

LSF files are always UTF-8 encoded.

## Installing

    pip install lsf-lions-sectioned-format

## An example LSF File

    title: My Blog
    tags: blog
    
    This is my blog.
    
    == 2021-01-20 ==
    tags: blogpost datepage github
    date: 2021-01-20
    
    Today I uploaded my lsf module to PyPI.
    
    == 2021-01-18 ==
    tags: blogpost datepage holiday
    date: 2021-02-10
    
    Today was Martin Luther King Day.

This file has a header section, and two content sections (`2021-01-20`, `2021-01-18`).  All sections have keys and body text content.

## Example of Use

Here's reading an LSF file:

    import lsf
    
    L = lsf.loadfile("basic_blog.lsf")
    
    for section in L:
        print(section[lsf.TITLE])
        print("  " + section[lsf.KEYS].get("tags"))
        print("  " + str(len(section[lsf.BODY])) + " characters in body")

And adding a section:

    lsf.append(L, "A Title", {"date": "2021-01-19", "tags": "test"}, "This is a new entry.")

And saving to the file:

    lsf.savefile(L, "basic_blog.lsf")

## Section Dictionaries

Each section has a dictionary of the form:

    {TITLE: "...a title...",
     TITLELN: 10,
     KEYS: {"key1": "value 1", "key2": "value 2", ...},
     BODY: "Central\nBody\nText\n",
     BODYLN: 16}

...which corresponds to section:

    10. == ...a title... ==
    11. key1: value 1
    12. key2: value 2
        ...
    15. 
    16. Central
    17. Body
    18. Text

(The line numbers are not part of the source; They are supplied only so that you can see how TITLELN and BODYLN function.)


It's safe to manipulate data in place.

