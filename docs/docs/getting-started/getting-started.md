---
sidebar_position: 1
slug: /getting-started
---

# Getting Started
MetAMDB is an easy to use tool for all things atom mappings. Be it atom mapping search by reactions/metabolites or atom mapping generation for user-uploaded models.

## Atom Mapping Formats
Atom mappings are accessible in three distinct formats: **RXN Files**, **Reaction Images** and the **ABC-Format**. 

### RXN Files
RXN Files are a type of [:link: Chemical Table File](https://en.wikipedia.org/wiki/Chemical_table_file) created by "MDL Information Systems". They can easily store atom mapping information for single reactions, include further information and can be comfortably read. Specifics about RXN Files [can be found in the documentation!](/metamdb-docs/rxn-file)

### Reaction Images
Reaction Images are visual representations of a given reaction and their atom mapping. These visualizations make it easy for a beginner to identify atom mappings in a otherwise complex RXN File. Further explanations of reaction images [can be found here!](/metamdb-docs/reaction-image)

### ABC-Format
```Glucose (abcdef) -> Glucose-6-phosphate (abcdef)```

The ABC-Format is a per element atom mapping representation, which for now can only display carbon mappings in MetAMDB. The mapping is depicted in parenthesis behind each metabolite and maps atoms based on the symbol used. For the above example the first glucose carbon (a) maps to the first glucose-6-phosphate carbon (a). The order of atoms for each metabolite depends on the order of atoms in their respective RXN Files. So the first carbon in the glucose MOL block of the above reaction would correspond to the first mapping atom.

## Model Based Atom Mappings
Atom mappings can be generated for user-uploaded **Reaction Models**. These atom mappings can be inspected and downloaded in the **Atom Mapping Model**.

**Reaction Models** are user-uploaded models of multiple reactions. Reactions and metabolites can be identified by specific database identifiers to get accurate atom mapping data, while manual atom mappings can be used for your custom or simplified reactions. [You can read about the specifications and more here!](/metamdb-docs/reaction-model)

## Database Query
**Database Searches** can be performed to find specific **Reactions** and their atom mappings in the RXN and image format. Reactions also incorporate additional information like database identifiers and their respective **Metabolites**. Everything about database searches [can be found here!](/metamdb-docs/database-search)
