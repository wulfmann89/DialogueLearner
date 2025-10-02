# DialogueLearner
Uses public-domain sources to seed a machine learning model used in a chat bot to help think through dialogue for story writing.  Builds contextual understanding of character traits over time with use.

# Overview of Architecture
- Using Project Gutenberg and Mozilla Common Language, chats with the user for natural, stylized dialogue based on character traits.
- maps character traits like anxious, charismatic, etc. to linguistic features and conversational tendencies.
- Generates speech patterns based on selected traits and story context.
- Progressively adapts phrasing and question prompts bvased on usage and feedback
- Attempts to use language samples from public domain using metadata and licensing headers.
- Use real world languages as a template to build novel fantasy languages

# Structure
/corpus_seed/                   # Public domain texts (filtered)
/scripts/                       # Corpus filtering and trait tagging
/traits/                        # Trait definitions and mappings
/dialogue_engine/               # Generation logic
/progressive_learning/          # Usage tracking and adaptation
/tests/                         # Unit tests and validation
README.md                       # Project overview

# Examples of traits:

Anxious: Hedging, repetition, short sentences
Charasmatic: Metaphros, grandiosity, rhythmic and positive

# Scope
- Tool for personal use only
- No external calls or cloud dependencies
- Learning is all local
