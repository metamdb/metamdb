---
sidebar_position: 1
slug: /database-search
---

# Database Search

The database can be queried for reaction names as well as metabolites but also pathway identifiers and pathway names. The type of query can be changed by clicking on the dropdown menu. The search is performed with a fuzzy match algorithm, meaning that patterns are matched (Glucose :arrow_right: D-Glucose/Glucose-6-phosphate). After successfully searching the database for reactions or metabolites a table with the following columns is displayed:
- [Name](/metamdb-docs/database-search#reaction-name)
- [Reaction ID](/metamdb-docs/database-search#reaction-id)
- [Formula](/metamdb-docs/database-search#formula)
- [Curated](/metamdb-docs/database-search#curated)
  
If the database is searched for pathways the following columns are displayed:
- [Name](/metamdb-docs/database-search#pathway-name)
- [Pathway ID](/metamdb-docs/database-search#reaction-id)
- [Identifier](/metamdb-docs/database-search#identifier)
- [Source](/metamdb-docs/database-search#source)

## Reaction Name
The name column contains all database identifiers corresponding to the found reaction. 

## Reaction ID
Reaction identifiers of the MetAMDB database are displayed here with links to the respective [Reaction](/metamdb-docs/reaction) pages. The table is sortable by reaction identifiers.

## Formula
Depicted here are the formula of their respective reactions.

## Curated
The curated column indicates the atom mapping status of each reaction:
- :heavy_check_mark: Manually curated
- :x: Automatically generated

The search results can be sorted by curation status.

## Pathway Name
The pathway name corresponds to the names given to each pathway by the source database.

## Pathway ID
Pathway identifiers of the MetAMDB database are linked to their respective [Pathway](/metamdb-docs/pathway) pages. The table is sortable by pathway identifiers

## Identifier
Pathway identifiers of their respective source databases. Table can be sorted by source identifiers.

## Source
The source database of the corresponding pathway entries. The table is sortable by source database.

