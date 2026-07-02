window.DHARMA_GRAPH = {
  "metadata": {
    "title": "Dharma Knowledge Graph",
    "version": "0.1",
    "generated_at": "2026-07-02T09:57:11.273667+00:00",
    "source_files": [
      "data/seeds/concepts.json",
      "data/seeds/core.json",
      "data/seeds/dhammapada.json",
      "data/seeds/heart_sutra.json",
      "data/seeds/places_traditions.json",
      "data/seeds/terms.json",
      "data/seeds/terms_extended.json"
    ]
  },
  "summary": {
    "node_count": 104,
    "relationship_count": 163,
    "node_type_counts": {
      "Citation": 17,
      "Concept": 37,
      "Person": 1,
      "Place": 6,
      "School": 5,
      "Term": 35,
      "Text": 3
    },
    "relationship_type_counts": {
      "AUTHORED_BY": 1,
      "BELONGS_TO_SCHOOL": 13,
      "CITES": 17,
      "DEFINES": 42,
      "LOCATED_IN": 4,
      "MENTIONS": 56,
      "RELATED_TO": 30
    }
  },
  "nodes": [
    {
      "id": "citation_dhammapada_1",
      "type": "Citation",
      "name": "Dhammapada 1",
      "source": "Dhammapada",
      "locator": "Verse 1",
      "notes": "Pilot citation for the relation between mind, intention, and suffering.",
      "source_file": "data/seeds/dhammapada.json"
    },
    {
      "id": "citation_dhammapada_129",
      "type": "Citation",
      "name": "Dhammapada 129",
      "source": "Dhammapada",
      "locator": "Verse 129",
      "notes": "Pilot citation for non-harming and empathy toward beings.",
      "source_file": "data/seeds/dhammapada.json"
    },
    {
      "id": "citation_dhammapada_183",
      "type": "Citation",
      "name": "Dhammapada 183",
      "source": "Dhammapada",
      "locator": "Verse 183",
      "notes": "Pilot citation for ethical restraint, wholesome cultivation, and mental purification.",
      "source_file": "data/seeds/dhammapada.json"
    },
    {
      "id": "citation_dhammapada_2",
      "type": "Citation",
      "name": "Dhammapada 2",
      "source": "Dhammapada",
      "locator": "Verse 2",
      "notes": "Pilot citation for the relation between mind, intention, and well-being.",
      "source_file": "data/seeds/dhammapada.json"
    },
    {
      "id": "citation_dhammapada_21",
      "type": "Citation",
      "name": "Dhammapada 21",
      "source": "Dhammapada",
      "locator": "Verse 21",
      "notes": "Pilot citation for heedfulness as a path quality.",
      "source_file": "data/seeds/dhammapada.json"
    },
    {
      "id": "citation_dhammapada_277",
      "type": "Citation",
      "name": "Dhammapada 277",
      "source": "Dhammapada",
      "locator": "Verse 277",
      "notes": "Pilot citation for impermanence.",
      "source_file": "data/seeds/dhammapada.json"
    },
    {
      "id": "citation_dhammapada_279",
      "type": "Citation",
      "name": "Dhammapada 279",
      "source": "Dhammapada",
      "locator": "Verse 279",
      "notes": "Pilot citation for not-self.",
      "source_file": "data/seeds/dhammapada.json"
    },
    {
      "id": "citation_dhammapada_35",
      "type": "Citation",
      "name": "Dhammapada 35",
      "source": "Dhammapada",
      "locator": "Verse 35",
      "notes": "Pilot citation for the training and restraint of mind.",
      "source_file": "data/seeds/dhammapada.json"
    },
    {
      "id": "citation_dhammapada_5",
      "type": "Citation",
      "name": "Dhammapada 5",
      "source": "Dhammapada",
      "locator": "Verse 5",
      "notes": "Pilot citation for non-hatred and reconciliation.",
      "source_file": "data/seeds/dhammapada.json"
    },
    {
      "id": "citation_dhammapada_50",
      "type": "Citation",
      "name": "Dhammapada 50",
      "source": "Dhammapada",
      "locator": "Verse 50",
      "notes": "Pilot citation for self-examination in ethical practice.",
      "source_file": "data/seeds/dhammapada.json"
    },
    {
      "id": "citation_heart_sutra_dharmas",
      "type": "Citation",
      "name": "Heart Sutra Dharmas Passage",
      "source": "Heart Sutra",
      "locator": "Dharmas and categories passage",
      "notes": "Pilot citation for sense bases, elements, dependent arising categories, and the four truths.",
      "source_file": "data/seeds/heart_sutra.json"
    },
    {
      "id": "citation_heart_sutra_mantra",
      "type": "Citation",
      "name": "Heart Sutra Mantra Passage",
      "source": "Heart Sutra",
      "locator": "Mantra passage",
      "notes": "Pilot citation for mantra and prajnaparamita as a practice expression.",
      "source_file": "data/seeds/heart_sutra.json"
    },
    {
      "id": "citation_heart_sutra_opening",
      "type": "Citation",
      "name": "Heart Sutra Opening",
      "source": "Heart Sutra",
      "locator": "Opening scene",
      "notes": "Pilot citation for Avalokitesvara, prajnaparamita, and the five aggregates.",
      "source_file": "data/seeds/heart_sutra.json"
    },
    {
      "id": "citation_heart_sutra_skandhas",
      "type": "Citation",
      "name": "Heart Sutra Skandhas Passage",
      "source": "Heart Sutra",
      "locator": "Five aggregates passage",
      "notes": "Pilot citation for the relationship between form, the aggregates, and emptiness.",
      "source_file": "data/seeds/heart_sutra.json"
    },
    {
      "id": "citation_mmkv_24_18",
      "type": "Citation",
      "name": "Mulamadhyamakakarika 24.18",
      "source": "Mulamadhyamakakarika",
      "locator": "Chapter 24, verse 18",
      "notes": "Pilot citation for dependent designation, emptiness, and the middle way.",
      "source_file": "data/seeds/core.json"
    },
    {
      "id": "citation_mmkv_24_19",
      "type": "Citation",
      "name": "Mulamadhyamakakarika 24.19",
      "source": "Mulamadhyamakakarika",
      "locator": "Chapter 24, verse 19",
      "notes": "Pilot citation for the relation between dependent arising and emptiness.",
      "source_file": "data/seeds/core.json"
    },
    {
      "id": "citation_mmkv_25_19",
      "type": "Citation",
      "name": "Mulamadhyamakakarika 25.19",
      "source": "Mulamadhyamakakarika",
      "locator": "Chapter 25, verse 19",
      "notes": "Pilot citation for the relation between samsara and nirvana in Madhyamaka analysis.",
      "source_file": "data/seeds/core.json"
    },
    {
      "id": "concept_ahimsa",
      "type": "Concept",
      "name": "Ahimsa",
      "pali": "avihimsa",
      "sanskrit": "ahimsa",
      "category": "ethics",
      "description": "Non-harming; an ethical orientation of restraint from violence and injury.",
      "source_file": "data/seeds/dhammapada.json"
    },
    {
      "id": "concept_anatta",
      "type": "Concept",
      "name": "Anatta",
      "pali": "anatta",
      "sanskrit": "anatman",
      "category": "doctrine",
      "description": "Not-self; the absence of a permanent, independent self in conditioned phenomena.",
      "source_file": "data/seeds/concepts.json"
    },
    {
      "id": "concept_anicca",
      "type": "Concept",
      "name": "Anicca",
      "pali": "anicca",
      "sanskrit": "anitya",
      "category": "doctrine",
      "description": "Impermanence; the conditioned nature of phenomena as changing and unstable.",
      "source_file": "data/seeds/concepts.json"
    },
    {
      "id": "concept_appamada",
      "type": "Concept",
      "name": "Appamada",
      "pali": "appamada",
      "sanskrit": "apramada",
      "category": "practice",
      "description": "Heedfulness or diligent care in practice.",
      "source_file": "data/seeds/dhammapada.json"
    },
    {
      "id": "concept_avalokitesvara",
      "type": "Concept",
      "name": "Avalokitesvara",
      "sanskrit": "avalokitesvara",
      "category": "mahayana",
      "description": "A bodhisattva associated with compassion and prominent in the Heart Sutra setting.",
      "source_file": "data/seeds/heart_sutra.json"
    },
    {
      "id": "concept_avidya",
      "type": "Concept",
      "name": "Avidya",
      "pali": "avijja",
      "sanskrit": "avidya",
      "category": "psychology",
      "description": "Ignorance or misknowing, especially regarding the nature of reality and the path.",
      "source_file": "data/seeds/concepts.json"
    },
    {
      "id": "concept_bodhicitta",
      "type": "Concept",
      "name": "Bodhicitta",
      "sanskrit": "bodhicitta",
      "category": "mahayana",
      "description": "The awakened mind or aspiration to attain awakening for the benefit of all beings.",
      "source_file": "data/seeds/concepts.json"
    },
    {
      "id": "concept_bodhisattva",
      "type": "Concept",
      "name": "Bodhisattva",
      "pali": "bodhisatta",
      "sanskrit": "bodhisattva",
      "category": "mahayana",
      "description": "A being oriented toward awakening, especially for the liberation of all beings in Mahayana contexts.",
      "source_file": "data/seeds/concepts.json"
    },
    {
      "id": "concept_brahmaviharas",
      "type": "Concept",
      "name": "Brahmaviharas",
      "pali": "brahmavihara",
      "sanskrit": "brahmavihara",
      "category": "practice",
      "description": "The four divine abodes: loving-kindness, compassion, sympathetic joy, and equanimity.",
      "source_file": "data/seeds/concepts.json"
    },
    {
      "id": "concept_citta",
      "type": "Concept",
      "name": "Citta",
      "pali": "citta",
      "sanskrit": "citta",
      "category": "psychology",
      "description": "Mind, heart, or mental orientation; a key term for understanding intention and experience.",
      "source_file": "data/seeds/dhammapada.json"
    },
    {
      "id": "concept_dukkha",
      "type": "Concept",
      "name": "Dukkha",
      "pali": "dukkha",
      "sanskrit": "duhkha",
      "description": "A central Dharma concept often translated as suffering, unsatisfactoriness, or stress.",
      "source_file": "data/seeds/core.json"
    },
    {
      "id": "concept_dhatu",
      "type": "Concept",
      "name": "Elements",
      "pali": "dhatu",
      "sanskrit": "dhatu",
      "category": "analysis",
      "description": "Elements or domains used to analyze experience and phenomena.",
      "source_file": "data/seeds/concepts.json"
    },
    {
      "id": "concept_skandhas",
      "type": "Concept",
      "name": "Five Aggregates",
      "pali": "khandha",
      "sanskrit": "skandha",
      "category": "analysis",
      "description": "Form, feeling, perception, formations, and consciousness as a framework for analyzing experience.",
      "source_file": "data/seeds/concepts.json"
    },
    {
      "id": "concept_form",
      "type": "Concept",
      "name": "Form",
      "pali": "rupa",
      "sanskrit": "rupa",
      "category": "analysis",
      "description": "Material form; one of the five aggregates.",
      "source_file": "data/seeds/heart_sutra.json"
    },
    {
      "id": "concept_four_noble_truths",
      "type": "Concept",
      "name": "Four Noble Truths",
      "pali": "cattari ariyasaccani",
      "sanskrit": "catvari aryasatyani",
      "category": "doctrine",
      "description": "The teaching of suffering, its origin, its cessation, and the path leading to cessation.",
      "source_file": "data/seeds/concepts.json"
    },
    {
      "id": "concept_karma",
      "type": "Concept",
      "name": "Karma",
      "pali": "kamma",
      "sanskrit": "karma",
      "category": "ethics",
      "description": "Intentional action and its ethical consequences.",
      "source_file": "data/seeds/concepts.json"
    },
    {
      "id": "concept_karuna",
      "type": "Concept",
      "name": "Karuna",
      "pali": "karuna",
      "sanskrit": "karuna",
      "category": "practice",
      "description": "Compassion; the wish for beings to be free from suffering.",
      "source_file": "data/seeds/concepts.json"
    },
    {
      "id": "concept_klesha",
      "type": "Concept",
      "name": "Klesha",
      "pali": "kilesa",
      "sanskrit": "klesa",
      "category": "psychology",
      "description": "Afflictive mental states that disturb the mind and condition suffering.",
      "source_file": "data/seeds/concepts.json"
    },
    {
      "id": "concept_mantra",
      "type": "Concept",
      "name": "Mantra",
      "sanskrit": "mantra",
      "category": "practice",
      "description": "A sacred utterance or formula used in contemplative and ritual contexts.",
      "source_file": "data/seeds/heart_sutra.json"
    },
    {
      "id": "concept_metta",
      "type": "Concept",
      "name": "Metta",
      "pali": "metta",
      "sanskrit": "maitri",
      "category": "practice",
      "description": "Loving-kindness; the cultivation of goodwill and friendliness.",
      "source_file": "data/seeds/concepts.json"
    },
    {
      "id": "concept_middle_way",
      "type": "Concept",
      "name": "Middle Way",
      "pali": "majjhima patipada",
      "sanskrit": "madhyama pratipad",
      "category": "practice",
      "description": "A path avoiding extremes, often framed as avoiding indulgence and self-mortification or eternalism and nihilism.",
      "source_file": "data/seeds/concepts.json"
    },
    {
      "id": "concept_mudita",
      "type": "Concept",
      "name": "Mudita",
      "pali": "mudita",
      "sanskrit": "mudita",
      "category": "practice",
      "description": "Sympathetic joy; delight in the welfare and happiness of others.",
      "source_file": "data/seeds/concepts.json"
    },
    {
      "id": "concept_nirvana",
      "type": "Concept",
      "name": "Nirvana",
      "pali": "nibbana",
      "sanskrit": "nirvana",
      "category": "liberation",
      "description": "Liberation; the extinguishing of greed, hatred, and delusion.",
      "source_file": "data/seeds/concepts.json"
    },
    {
      "id": "concept_noble_eightfold_path",
      "type": "Concept",
      "name": "Noble Eightfold Path",
      "pali": "ariya atthangika magga",
      "sanskrit": "arya astangika marga",
      "category": "practice",
      "description": "The path of right view, intention, speech, action, livelihood, effort, mindfulness, and concentration.",
      "source_file": "data/seeds/concepts.json"
    },
    {
      "id": "concept_paramita",
      "type": "Concept",
      "name": "Paramita",
      "pali": "parami",
      "sanskrit": "paramita",
      "category": "mahayana",
      "description": "Perfection or transcendent virtue cultivated on the bodhisattva path.",
      "source_file": "data/seeds/concepts.json"
    },
    {
      "id": "concept_prajna",
      "type": "Concept",
      "name": "Prajna",
      "pali": "panna",
      "sanskrit": "prajna",
      "category": "wisdom",
      "description": "Wisdom or liberating insight into the nature of phenomena.",
      "source_file": "data/seeds/concepts.json"
    },
    {
      "id": "concept_prajnaparamita",
      "type": "Concept",
      "name": "Prajnaparamita",
      "sanskrit": "prajnaparamita",
      "category": "mahayana",
      "description": "The perfection of wisdom; a central theme in Mahayana sutra literature.",
      "source_file": "data/seeds/heart_sutra.json"
    },
    {
      "id": "concept_pratityasamutpada",
      "type": "Concept",
      "name": "Pratityasamutpada",
      "pali": "paticcasamuppada",
      "sanskrit": "pratityasamutpada",
      "category": "doctrine",
      "description": "Dependent arising; the principle that phenomena arise in dependence on causes and conditions.",
      "source_file": "data/seeds/concepts.json"
    },
    {
      "id": "concept_samadhi",
      "type": "Concept",
      "name": "Samadhi",
      "pali": "samadhi",
      "sanskrit": "samadhi",
      "category": "practice",
      "description": "Collectedness, concentration, or meditative absorption.",
      "source_file": "data/seeds/concepts.json"
    },
    {
      "id": "concept_samsara",
      "type": "Concept",
      "name": "Samsara",
      "pali": "samsara",
      "sanskrit": "samsara",
      "category": "cosmology",
      "description": "The cycle of birth, death, and rebirth conditioned by ignorance and craving.",
      "source_file": "data/seeds/concepts.json"
    },
    {
      "id": "concept_sila",
      "type": "Concept",
      "name": "Sila",
      "pali": "sila",
      "sanskrit": "sila",
      "category": "ethics",
      "description": "Ethical conduct or moral discipline.",
      "source_file": "data/seeds/concepts.json"
    },
    {
      "id": "concept_ayatana",
      "type": "Concept",
      "name": "Six Sense Bases",
      "pali": "ayatana",
      "sanskrit": "ayatana",
      "category": "analysis",
      "description": "The internal and external sense bases involved in perceptual experience.",
      "source_file": "data/seeds/concepts.json"
    },
    {
      "id": "concept_sunyata",
      "type": "Concept",
      "name": "Sunyata",
      "sanskrit": "sunyata",
      "description": "A Mahayana concept commonly translated as emptiness.",
      "source_file": "data/seeds/core.json"
    },
    {
      "id": "concept_tanha",
      "type": "Concept",
      "name": "Tanha",
      "pali": "tanha",
      "sanskrit": "trsna",
      "category": "psychology",
      "description": "Craving or thirst; a central condition in the arising of suffering.",
      "source_file": "data/seeds/concepts.json"
    },
    {
      "id": "concept_three_marks",
      "type": "Concept",
      "name": "Three Marks of Existence",
      "pali": "tilakkhana",
      "sanskrit": "trilaksana",
      "category": "doctrine",
      "description": "The marks of impermanence, suffering or unsatisfactoriness, and not-self.",
      "source_file": "data/seeds/concepts.json"
    },
    {
      "id": "concept_two_truths",
      "type": "Concept",
      "name": "Two Truths",
      "sanskrit": "satya-dvaya",
      "category": "mahayana",
      "description": "The distinction between conventional truth and ultimate truth.",
      "source_file": "data/seeds/concepts.json"
    },
    {
      "id": "concept_upekkha",
      "type": "Concept",
      "name": "Upekkha",
      "pali": "upekkha",
      "sanskrit": "upeksa",
      "category": "practice",
      "description": "Equanimity; balanced presence toward changing experience.",
      "source_file": "data/seeds/concepts.json"
    },
    {
      "id": "person_nagarjuna",
      "type": "Person",
      "name": "Nagarjuna",
      "tradition": "Mahayana",
      "description": "A major Buddhist philosopher associated with Madhyamaka.",
      "source_file": "data/seeds/core.json"
    },
    {
      "id": "place_bodh_gaya",
      "type": "Place",
      "name": "Bodh Gaya",
      "country": "India",
      "region": "Bihar",
      "description": "A major Buddhist pilgrimage place associated with the Buddha's awakening.",
      "source_file": "data/seeds/places_traditions.json"
    },
    {
      "id": "place_gandhara",
      "type": "Place",
      "name": "Gandhara",
      "country": "Historical region",
      "region": "Northwest South Asia",
      "description": "A historical Buddhist region important for textual and artistic transmission.",
      "source_file": "data/seeds/places_traditions.json"
    },
    {
      "id": "place_magadha",
      "type": "Place",
      "name": "Magadha",
      "country": "India",
      "region": "Eastern India",
      "description": "An ancient region important in early Buddhist history.",
      "source_file": "data/seeds/places_traditions.json"
    },
    {
      "id": "place_nalanda",
      "type": "Place",
      "name": "Nalanda",
      "country": "India",
      "region": "Bihar",
      "description": "A historic center of Buddhist monastic learning.",
      "source_file": "data/seeds/places_traditions.json"
    },
    {
      "id": "place_sarnath",
      "type": "Place",
      "name": "Sarnath",
      "country": "India",
      "region": "Uttar Pradesh",
      "description": "A major Buddhist pilgrimage place associated with the first teaching.",
      "source_file": "data/seeds/places_traditions.json"
    },
    {
      "id": "place_sri_lanka",
      "type": "Place",
      "name": "Sri Lanka",
      "country": "Sri Lanka",
      "region": "South Asia",
      "description": "A major historical center for Theravada Buddhist transmission.",
      "source_file": "data/seeds/places_traditions.json"
    },
    {
      "id": "school_early_buddhism",
      "type": "School",
      "name": "Early Buddhism",
      "description": "A working category for early Buddhist teachings and textual layers.",
      "source_file": "data/seeds/places_traditions.json"
    },
    {
      "id": "school_madhyamaka",
      "type": "School",
      "name": "Madhyamaka",
      "description": "A Mahayana philosophical school associated with analysis of emptiness.",
      "source_file": "data/seeds/core.json"
    },
    {
      "id": "school_mahayana",
      "type": "School",
      "name": "Mahayana",
      "description": "A broad family of Buddhist traditions emphasizing the bodhisattva path.",
      "source_file": "data/seeds/places_traditions.json"
    },
    {
      "id": "school_pali_canon",
      "type": "School",
      "name": "Pali Canon",
      "description": "A textual tradition preserving canonical materials in Pali.",
      "source_file": "data/seeds/places_traditions.json"
    },
    {
      "id": "school_theravada",
      "type": "School",
      "name": "Theravada",
      "description": "A Buddhist tradition preserving the Pali Canon.",
      "source_file": "data/seeds/core.json"
    },
    {
      "id": "term_anatman_sanskrit",
      "type": "Term",
      "name": "anatman",
      "language": "Sanskrit",
      "script": "Latin",
      "transliteration": "anatman",
      "translation": "not-self; no self",
      "notes": "Sanskrit form corresponding to Pali anatta.",
      "source_file": "data/seeds/terms.json"
    },
    {
      "id": "term_anatta_pali",
      "type": "Term",
      "name": "anatta",
      "language": "Pali",
      "script": "Latin",
      "transliteration": "anatta",
      "translation": "not-self",
      "notes": "Pali form used for the doctrine of not-self.",
      "source_file": "data/seeds/terms.json"
    },
    {
      "id": "term_anicca_pali",
      "type": "Term",
      "name": "anicca",
      "language": "Pali",
      "script": "Latin",
      "transliteration": "anicca",
      "translation": "impermanent",
      "notes": "Pali form used for impermanence.",
      "source_file": "data/seeds/terms.json"
    },
    {
      "id": "term_anitya_sanskrit",
      "type": "Term",
      "name": "anitya",
      "language": "Sanskrit",
      "script": "Latin",
      "transliteration": "anitya",
      "translation": "impermanent",
      "notes": "Sanskrit form used for impermanence.",
      "source_file": "data/seeds/terms.json"
    },
    {
      "id": "term_appamada_pali",
      "type": "Term",
      "name": "appamada",
      "language": "Pali",
      "script": "Latin",
      "transliteration": "appamada",
      "translation": "heedfulness; diligence",
      "notes": "A central practice quality highlighted in the Dhammapada.",
      "source_file": "data/seeds/terms.json"
    },
    {
      "id": "term_avidya_sanskrit",
      "type": "Term",
      "name": "avidya",
      "language": "Sanskrit",
      "script": "Latin",
      "transliteration": "avidya",
      "translation": "ignorance",
      "notes": "Sanskrit term for ignorance or misknowing.",
      "source_file": "data/seeds/terms_extended.json"
    },
    {
      "id": "term_avijja_pali",
      "type": "Term",
      "name": "avijja",
      "language": "Pali",
      "script": "Latin",
      "transliteration": "avijja",
      "translation": "ignorance",
      "notes": "Pali term for ignorance or misknowing.",
      "source_file": "data/seeds/terms_extended.json"
    },
    {
      "id": "term_ayatana_pali",
      "type": "Term",
      "name": "ayatana",
      "language": "Pali",
      "script": "Latin",
      "transliteration": "ayatana",
      "translation": "sense base",
      "notes": "Pali and Sanskrit term for sense base.",
      "source_file": "data/seeds/terms_extended.json"
    },
    {
      "id": "term_bodhicitta_sanskrit",
      "type": "Term",
      "name": "bodhicitta",
      "language": "Sanskrit",
      "script": "Latin",
      "transliteration": "bodhicitta",
      "translation": "awakening mind",
      "notes": "Sanskrit term for the awakened mind or aspiration toward awakening.",
      "source_file": "data/seeds/terms_extended.json"
    },
    {
      "id": "term_bodhisattva_sanskrit",
      "type": "Term",
      "name": "bodhisattva",
      "language": "Sanskrit",
      "script": "Latin",
      "transliteration": "bodhisattva",
      "translation": "awakening being",
      "notes": "Sanskrit term for a being oriented toward awakening.",
      "source_file": "data/seeds/terms_extended.json"
    },
    {
      "id": "term_citta_pali",
      "type": "Term",
      "name": "citta",
      "language": "Pali",
      "script": "Latin",
      "transliteration": "citta",
      "translation": "mind; heart",
      "notes": "A term for mind, heart, or mental orientation.",
      "source_file": "data/seeds/terms.json"
    },
    {
      "id": "term_dhatu_pali",
      "type": "Term",
      "name": "dhatu",
      "language": "Pali",
      "script": "Latin",
      "transliteration": "dhatu",
      "translation": "element; domain",
      "notes": "Pali and Sanskrit term for element or domain.",
      "source_file": "data/seeds/terms_extended.json"
    },
    {
      "id": "term_duhkha_sanskrit",
      "type": "Term",
      "name": "duhkha",
      "language": "Sanskrit",
      "script": "Latin",
      "transliteration": "duhkha",
      "translation": "suffering; unsatisfactoriness",
      "notes": "Sanskrit cognate of Pali dukkha.",
      "source_file": "data/seeds/terms.json"
    },
    {
      "id": "term_dukkha_pali",
      "type": "Term",
      "name": "dukkha",
      "language": "Pali",
      "script": "Latin",
      "transliteration": "dukkha",
      "translation": "suffering; unsatisfactoriness; stress",
      "notes": "A core Pali term in the analysis of conditioned experience.",
      "source_file": "data/seeds/terms.json"
    },
    {
      "id": "term_kamma_pali",
      "type": "Term",
      "name": "kamma",
      "language": "Pali",
      "script": "Latin",
      "transliteration": "kamma",
      "translation": "intentional action",
      "notes": "Pali form corresponding to Sanskrit karma.",
      "source_file": "data/seeds/terms_extended.json"
    },
    {
      "id": "term_karma_sanskrit",
      "type": "Term",
      "name": "karma",
      "language": "Sanskrit",
      "script": "Latin",
      "transliteration": "karma",
      "translation": "intentional action",
      "notes": "Sanskrit form for intentional action and its consequences.",
      "source_file": "data/seeds/terms_extended.json"
    },
    {
      "id": "term_karuna_pali",
      "type": "Term",
      "name": "karuna",
      "language": "Pali",
      "script": "Latin",
      "transliteration": "karuna",
      "translation": "compassion",
      "notes": "Pali and Sanskrit term for compassion.",
      "source_file": "data/seeds/terms.json"
    },
    {
      "id": "term_mantra_sanskrit",
      "type": "Term",
      "name": "mantra",
      "language": "Sanskrit",
      "script": "Latin",
      "transliteration": "mantra",
      "translation": "sacred utterance",
      "notes": "Sanskrit term for a sacred utterance or formula.",
      "source_file": "data/seeds/terms_extended.json"
    },
    {
      "id": "term_metta_pali",
      "type": "Term",
      "name": "metta",
      "language": "Pali",
      "script": "Latin",
      "transliteration": "metta",
      "translation": "loving-kindness",
      "notes": "Pali term for loving-kindness.",
      "source_file": "data/seeds/terms.json"
    },
    {
      "id": "term_nibbana_pali",
      "type": "Term",
      "name": "nibbana",
      "language": "Pali",
      "script": "Latin",
      "transliteration": "nibbana",
      "translation": "liberation; extinguishing",
      "notes": "Pali term commonly rendered as nirvana.",
      "source_file": "data/seeds/terms.json"
    },
    {
      "id": "term_nirvana_sanskrit",
      "type": "Term",
      "name": "nirvana",
      "language": "Sanskrit",
      "script": "Latin",
      "transliteration": "nirvana",
      "translation": "liberation; extinguishing",
      "notes": "Sanskrit form corresponding to Pali nibbana.",
      "source_file": "data/seeds/terms.json"
    },
    {
      "id": "term_panna_pali",
      "type": "Term",
      "name": "panna",
      "language": "Pali",
      "script": "Latin",
      "transliteration": "panna",
      "translation": "wisdom",
      "notes": "Pali term corresponding to Sanskrit prajna.",
      "source_file": "data/seeds/terms_extended.json"
    },
    {
      "id": "term_paramita_sanskrit",
      "type": "Term",
      "name": "paramita",
      "language": "Sanskrit",
      "script": "Latin",
      "transliteration": "paramita",
      "translation": "perfection",
      "notes": "Sanskrit term for perfection or transcendent virtue.",
      "source_file": "data/seeds/terms_extended.json"
    },
    {
      "id": "term_paticcasamuppada_pali",
      "type": "Term",
      "name": "paticcasamuppada",
      "language": "Pali",
      "script": "Latin",
      "transliteration": "paticcasamuppada",
      "translation": "dependent arising",
      "notes": "Pali term for dependent arising.",
      "source_file": "data/seeds/terms.json"
    },
    {
      "id": "term_prajna_sanskrit",
      "type": "Term",
      "name": "prajna",
      "language": "Sanskrit",
      "script": "Latin",
      "transliteration": "prajna",
      "translation": "wisdom",
      "notes": "Sanskrit term for wisdom or liberating insight.",
      "source_file": "data/seeds/terms_extended.json"
    },
    {
      "id": "term_prajnaparamita_sanskrit",
      "type": "Term",
      "name": "prajnaparamita",
      "language": "Sanskrit",
      "script": "Latin",
      "transliteration": "prajnaparamita",
      "translation": "perfection of wisdom",
      "notes": "Sanskrit term for the perfection of wisdom.",
      "source_file": "data/seeds/terms_extended.json"
    },
    {
      "id": "term_pratityasamutpada_sanskrit",
      "type": "Term",
      "name": "pratityasamutpada",
      "language": "Sanskrit",
      "script": "Latin",
      "transliteration": "pratityasamutpada",
      "translation": "dependent arising",
      "notes": "Sanskrit term for dependent arising.",
      "source_file": "data/seeds/terms.json"
    },
    {
      "id": "term_rupa_pali",
      "type": "Term",
      "name": "rupa",
      "language": "Pali",
      "script": "Latin",
      "transliteration": "rupa",
      "translation": "form; material form",
      "notes": "Pali and Sanskrit term for form.",
      "source_file": "data/seeds/terms_extended.json"
    },
    {
      "id": "term_samadhi_pali",
      "type": "Term",
      "name": "samadhi",
      "language": "Pali",
      "script": "Latin",
      "transliteration": "samadhi",
      "translation": "concentration; collectedness",
      "notes": "Pali and Sanskrit term for meditative collectedness.",
      "source_file": "data/seeds/terms_extended.json"
    },
    {
      "id": "term_samsara_pali",
      "type": "Term",
      "name": "samsara",
      "language": "Pali",
      "script": "Latin",
      "transliteration": "samsara",
      "translation": "cycle of rebirth",
      "notes": "Pali form for the cycle of conditioned existence.",
      "source_file": "data/seeds/terms_extended.json"
    },
    {
      "id": "term_sila_pali",
      "type": "Term",
      "name": "sila",
      "language": "Pali",
      "script": "Latin",
      "transliteration": "sila",
      "translation": "ethical conduct",
      "notes": "Pali term for moral discipline or ethical conduct.",
      "source_file": "data/seeds/terms_extended.json"
    },
    {
      "id": "term_skandha_sanskrit",
      "type": "Term",
      "name": "skandha",
      "language": "Sanskrit",
      "script": "Latin",
      "transliteration": "skandha",
      "translation": "aggregate",
      "notes": "Sanskrit term for aggregate.",
      "source_file": "data/seeds/terms_extended.json"
    },
    {
      "id": "term_sunyata_sanskrit",
      "type": "Term",
      "name": "sunyata",
      "language": "Sanskrit",
      "script": "Latin",
      "transliteration": "sunyata",
      "translation": "emptiness",
      "notes": "A key Mahayana term, especially important in Madhyamaka contexts.",
      "source_file": "data/seeds/terms.json"
    },
    {
      "id": "term_tanha_pali",
      "type": "Term",
      "name": "tanha",
      "language": "Pali",
      "script": "Latin",
      "transliteration": "tanha",
      "translation": "craving; thirst",
      "notes": "Pali term for craving.",
      "source_file": "data/seeds/terms_extended.json"
    },
    {
      "id": "term_trsna_sanskrit",
      "type": "Term",
      "name": "trsna",
      "language": "Sanskrit",
      "script": "Latin",
      "transliteration": "trsna",
      "translation": "craving; thirst",
      "notes": "Sanskrit term corresponding to Pali tanha.",
      "source_file": "data/seeds/terms_extended.json"
    },
    {
      "id": "text_dhammapada",
      "type": "Text",
      "name": "Dhammapada",
      "language": "Pali",
      "tradition": "Theravada",
      "description": "A collection of verses from the Pali Canon, traditionally arranged into 26 chapters.",
      "source_file": "data/seeds/dhammapada.json"
    },
    {
      "id": "text_heart_sutra",
      "type": "Text",
      "name": "Heart Sutra",
      "alternate_names": [
        "Prajnaparamita Hrdaya",
        "Heart of the Perfection of Wisdom"
      ],
      "language": "Sanskrit",
      "tradition": "Mahayana",
      "description": "A short Mahayana sutra associated with the perfection of wisdom literature and the teaching of emptiness.",
      "source_file": "data/seeds/heart_sutra.json"
    },
    {
      "id": "text_mulamadhyamakakarika",
      "type": "Text",
      "name": "Mulamadhyamakakarika",
      "language": "Sanskrit",
      "tradition": "Mahayana",
      "description": "A foundational Madhyamaka text attributed to Nagarjuna.",
      "source_file": "data/seeds/core.json"
    }
  ],
  "relationships": [
    {
      "source": "text_mulamadhyamakakarika",
      "type": "AUTHORED_BY",
      "target": "person_nagarjuna",
      "source_file": "data/seeds/core.json"
    },
    {
      "source": "concept_avalokitesvara",
      "type": "BELONGS_TO_SCHOOL",
      "target": "school_mahayana",
      "source_file": "data/seeds/heart_sutra.json"
    },
    {
      "source": "concept_bodhicitta",
      "type": "BELONGS_TO_SCHOOL",
      "target": "school_mahayana",
      "source_file": "data/seeds/places_traditions.json"
    },
    {
      "source": "concept_bodhisattva",
      "type": "BELONGS_TO_SCHOOL",
      "target": "school_mahayana",
      "source_file": "data/seeds/places_traditions.json"
    },
    {
      "source": "concept_prajnaparamita",
      "type": "BELONGS_TO_SCHOOL",
      "target": "school_mahayana",
      "source_file": "data/seeds/heart_sutra.json"
    },
    {
      "source": "concept_sunyata",
      "type": "BELONGS_TO_SCHOOL",
      "target": "school_mahayana",
      "source_file": "data/seeds/places_traditions.json"
    },
    {
      "source": "person_nagarjuna",
      "type": "BELONGS_TO_SCHOOL",
      "target": "school_madhyamaka",
      "source_file": "data/seeds/core.json"
    },
    {
      "source": "person_nagarjuna",
      "type": "BELONGS_TO_SCHOOL",
      "target": "school_mahayana",
      "source_file": "data/seeds/places_traditions.json"
    },
    {
      "source": "school_madhyamaka",
      "type": "BELONGS_TO_SCHOOL",
      "target": "school_mahayana",
      "source_file": "data/seeds/places_traditions.json"
    },
    {
      "source": "text_dhammapada",
      "type": "BELONGS_TO_SCHOOL",
      "target": "school_early_buddhism",
      "source_file": "data/seeds/places_traditions.json"
    },
    {
      "source": "text_dhammapada",
      "type": "BELONGS_TO_SCHOOL",
      "target": "school_pali_canon",
      "source_file": "data/seeds/places_traditions.json"
    },
    {
      "source": "text_dhammapada",
      "type": "BELONGS_TO_SCHOOL",
      "target": "school_theravada",
      "source_file": "data/seeds/dhammapada.json"
    },
    {
      "source": "text_heart_sutra",
      "type": "BELONGS_TO_SCHOOL",
      "target": "school_mahayana",
      "source_file": "data/seeds/heart_sutra.json"
    },
    {
      "source": "text_mulamadhyamakakarika",
      "type": "BELONGS_TO_SCHOOL",
      "target": "school_madhyamaka",
      "source_file": "data/seeds/places_traditions.json"
    },
    {
      "source": "text_dhammapada",
      "type": "CITES",
      "target": "citation_dhammapada_1",
      "source_file": "data/seeds/dhammapada.json"
    },
    {
      "source": "text_dhammapada",
      "type": "CITES",
      "target": "citation_dhammapada_129",
      "source_file": "data/seeds/dhammapada.json"
    },
    {
      "source": "text_dhammapada",
      "type": "CITES",
      "target": "citation_dhammapada_183",
      "source_file": "data/seeds/dhammapada.json"
    },
    {
      "source": "text_dhammapada",
      "type": "CITES",
      "target": "citation_dhammapada_2",
      "source_file": "data/seeds/dhammapada.json"
    },
    {
      "source": "text_dhammapada",
      "type": "CITES",
      "target": "citation_dhammapada_21",
      "source_file": "data/seeds/dhammapada.json"
    },
    {
      "source": "text_dhammapada",
      "type": "CITES",
      "target": "citation_dhammapada_277",
      "source_file": "data/seeds/dhammapada.json"
    },
    {
      "source": "text_dhammapada",
      "type": "CITES",
      "target": "citation_dhammapada_279",
      "source_file": "data/seeds/dhammapada.json"
    },
    {
      "source": "text_dhammapada",
      "type": "CITES",
      "target": "citation_dhammapada_35",
      "source_file": "data/seeds/dhammapada.json"
    },
    {
      "source": "text_dhammapada",
      "type": "CITES",
      "target": "citation_dhammapada_5",
      "source_file": "data/seeds/dhammapada.json"
    },
    {
      "source": "text_dhammapada",
      "type": "CITES",
      "target": "citation_dhammapada_50",
      "source_file": "data/seeds/dhammapada.json"
    },
    {
      "source": "text_heart_sutra",
      "type": "CITES",
      "target": "citation_heart_sutra_dharmas",
      "source_file": "data/seeds/heart_sutra.json"
    },
    {
      "source": "text_heart_sutra",
      "type": "CITES",
      "target": "citation_heart_sutra_mantra",
      "source_file": "data/seeds/heart_sutra.json"
    },
    {
      "source": "text_heart_sutra",
      "type": "CITES",
      "target": "citation_heart_sutra_opening",
      "source_file": "data/seeds/heart_sutra.json"
    },
    {
      "source": "text_heart_sutra",
      "type": "CITES",
      "target": "citation_heart_sutra_skandhas",
      "source_file": "data/seeds/heart_sutra.json"
    },
    {
      "source": "text_mulamadhyamakakarika",
      "type": "CITES",
      "target": "citation_mmkv_24_18",
      "source_file": "data/seeds/core.json"
    },
    {
      "source": "text_mulamadhyamakakarika",
      "type": "CITES",
      "target": "citation_mmkv_24_19",
      "source_file": "data/seeds/core.json"
    },
    {
      "source": "text_mulamadhyamakakarika",
      "type": "CITES",
      "target": "citation_mmkv_25_19",
      "source_file": "data/seeds/core.json"
    },
    {
      "source": "concept_brahmaviharas",
      "type": "DEFINES",
      "target": "concept_karuna",
      "source_file": "data/seeds/concepts.json"
    },
    {
      "source": "concept_brahmaviharas",
      "type": "DEFINES",
      "target": "concept_metta",
      "source_file": "data/seeds/concepts.json"
    },
    {
      "source": "concept_brahmaviharas",
      "type": "DEFINES",
      "target": "concept_mudita",
      "source_file": "data/seeds/concepts.json"
    },
    {
      "source": "concept_brahmaviharas",
      "type": "DEFINES",
      "target": "concept_upekkha",
      "source_file": "data/seeds/concepts.json"
    },
    {
      "source": "concept_three_marks",
      "type": "DEFINES",
      "target": "concept_anatta",
      "source_file": "data/seeds/concepts.json"
    },
    {
      "source": "concept_three_marks",
      "type": "DEFINES",
      "target": "concept_anicca",
      "source_file": "data/seeds/concepts.json"
    },
    {
      "source": "concept_three_marks",
      "type": "DEFINES",
      "target": "concept_dukkha",
      "source_file": "data/seeds/concepts.json"
    },
    {
      "source": "term_anatman_sanskrit",
      "type": "DEFINES",
      "target": "concept_anatta",
      "source_file": "data/seeds/terms.json"
    },
    {
      "source": "term_anatta_pali",
      "type": "DEFINES",
      "target": "concept_anatta",
      "source_file": "data/seeds/terms.json"
    },
    {
      "source": "term_anicca_pali",
      "type": "DEFINES",
      "target": "concept_anicca",
      "source_file": "data/seeds/terms.json"
    },
    {
      "source": "term_anitya_sanskrit",
      "type": "DEFINES",
      "target": "concept_anicca",
      "source_file": "data/seeds/terms.json"
    },
    {
      "source": "term_appamada_pali",
      "type": "DEFINES",
      "target": "concept_appamada",
      "source_file": "data/seeds/terms.json"
    },
    {
      "source": "term_avidya_sanskrit",
      "type": "DEFINES",
      "target": "concept_avidya",
      "source_file": "data/seeds/terms_extended.json"
    },
    {
      "source": "term_avijja_pali",
      "type": "DEFINES",
      "target": "concept_avidya",
      "source_file": "data/seeds/terms_extended.json"
    },
    {
      "source": "term_ayatana_pali",
      "type": "DEFINES",
      "target": "concept_ayatana",
      "source_file": "data/seeds/terms_extended.json"
    },
    {
      "source": "term_bodhicitta_sanskrit",
      "type": "DEFINES",
      "target": "concept_bodhicitta",
      "source_file": "data/seeds/terms_extended.json"
    },
    {
      "source": "term_bodhisattva_sanskrit",
      "type": "DEFINES",
      "target": "concept_bodhisattva",
      "source_file": "data/seeds/terms_extended.json"
    },
    {
      "source": "term_citta_pali",
      "type": "DEFINES",
      "target": "concept_citta",
      "source_file": "data/seeds/terms.json"
    },
    {
      "source": "term_dhatu_pali",
      "type": "DEFINES",
      "target": "concept_dhatu",
      "source_file": "data/seeds/terms_extended.json"
    },
    {
      "source": "term_duhkha_sanskrit",
      "type": "DEFINES",
      "target": "concept_dukkha",
      "source_file": "data/seeds/terms.json"
    },
    {
      "source": "term_dukkha_pali",
      "type": "DEFINES",
      "target": "concept_dukkha",
      "source_file": "data/seeds/terms.json"
    },
    {
      "source": "term_kamma_pali",
      "type": "DEFINES",
      "target": "concept_karma",
      "source_file": "data/seeds/terms_extended.json"
    },
    {
      "source": "term_karma_sanskrit",
      "type": "DEFINES",
      "target": "concept_karma",
      "source_file": "data/seeds/terms_extended.json"
    },
    {
      "source": "term_karuna_pali",
      "type": "DEFINES",
      "target": "concept_karuna",
      "source_file": "data/seeds/terms.json"
    },
    {
      "source": "term_mantra_sanskrit",
      "type": "DEFINES",
      "target": "concept_mantra",
      "source_file": "data/seeds/terms_extended.json"
    },
    {
      "source": "term_metta_pali",
      "type": "DEFINES",
      "target": "concept_metta",
      "source_file": "data/seeds/terms.json"
    },
    {
      "source": "term_nibbana_pali",
      "type": "DEFINES",
      "target": "concept_nirvana",
      "source_file": "data/seeds/terms.json"
    },
    {
      "source": "term_nirvana_sanskrit",
      "type": "DEFINES",
      "target": "concept_nirvana",
      "source_file": "data/seeds/terms.json"
    },
    {
      "source": "term_panna_pali",
      "type": "DEFINES",
      "target": "concept_prajna",
      "source_file": "data/seeds/terms_extended.json"
    },
    {
      "source": "term_paramita_sanskrit",
      "type": "DEFINES",
      "target": "concept_paramita",
      "source_file": "data/seeds/terms_extended.json"
    },
    {
      "source": "term_paticcasamuppada_pali",
      "type": "DEFINES",
      "target": "concept_pratityasamutpada",
      "source_file": "data/seeds/terms.json"
    },
    {
      "source": "term_prajna_sanskrit",
      "type": "DEFINES",
      "target": "concept_prajna",
      "source_file": "data/seeds/terms_extended.json"
    },
    {
      "source": "term_prajnaparamita_sanskrit",
      "type": "DEFINES",
      "target": "concept_prajnaparamita",
      "source_file": "data/seeds/terms_extended.json"
    },
    {
      "source": "term_pratityasamutpada_sanskrit",
      "type": "DEFINES",
      "target": "concept_pratityasamutpada",
      "source_file": "data/seeds/terms.json"
    },
    {
      "source": "term_rupa_pali",
      "type": "DEFINES",
      "target": "concept_form",
      "source_file": "data/seeds/terms_extended.json"
    },
    {
      "source": "term_samadhi_pali",
      "type": "DEFINES",
      "target": "concept_samadhi",
      "source_file": "data/seeds/terms_extended.json"
    },
    {
      "source": "term_samsara_pali",
      "type": "DEFINES",
      "target": "concept_samsara",
      "source_file": "data/seeds/terms_extended.json"
    },
    {
      "source": "term_sila_pali",
      "type": "DEFINES",
      "target": "concept_sila",
      "source_file": "data/seeds/terms_extended.json"
    },
    {
      "source": "term_skandha_sanskrit",
      "type": "DEFINES",
      "target": "concept_skandhas",
      "source_file": "data/seeds/terms_extended.json"
    },
    {
      "source": "term_sunyata_sanskrit",
      "type": "DEFINES",
      "target": "concept_sunyata",
      "source_file": "data/seeds/terms.json"
    },
    {
      "source": "term_tanha_pali",
      "type": "DEFINES",
      "target": "concept_tanha",
      "source_file": "data/seeds/terms_extended.json"
    },
    {
      "source": "term_trsna_sanskrit",
      "type": "DEFINES",
      "target": "concept_tanha",
      "source_file": "data/seeds/terms_extended.json"
    },
    {
      "source": "place_bodh_gaya",
      "type": "LOCATED_IN",
      "target": "place_magadha",
      "source_file": "data/seeds/places_traditions.json"
    },
    {
      "source": "place_nalanda",
      "type": "LOCATED_IN",
      "target": "place_magadha",
      "source_file": "data/seeds/places_traditions.json"
    },
    {
      "source": "school_pali_canon",
      "type": "LOCATED_IN",
      "target": "place_sri_lanka",
      "source_file": "data/seeds/places_traditions.json"
    },
    {
      "source": "school_theravada",
      "type": "LOCATED_IN",
      "target": "place_sri_lanka",
      "source_file": "data/seeds/places_traditions.json"
    },
    {
      "source": "citation_dhammapada_1",
      "type": "MENTIONS",
      "target": "concept_citta",
      "source_file": "data/seeds/dhammapada.json"
    },
    {
      "source": "citation_dhammapada_1",
      "type": "MENTIONS",
      "target": "concept_dukkha",
      "source_file": "data/seeds/dhammapada.json"
    },
    {
      "source": "citation_dhammapada_1",
      "type": "MENTIONS",
      "target": "concept_karma",
      "source_file": "data/seeds/dhammapada.json"
    },
    {
      "source": "citation_dhammapada_129",
      "type": "MENTIONS",
      "target": "concept_ahimsa",
      "source_file": "data/seeds/dhammapada.json"
    },
    {
      "source": "citation_dhammapada_129",
      "type": "MENTIONS",
      "target": "concept_karuna",
      "source_file": "data/seeds/dhammapada.json"
    },
    {
      "source": "citation_dhammapada_183",
      "type": "MENTIONS",
      "target": "concept_citta",
      "source_file": "data/seeds/dhammapada.json"
    },
    {
      "source": "citation_dhammapada_183",
      "type": "MENTIONS",
      "target": "concept_sila",
      "source_file": "data/seeds/dhammapada.json"
    },
    {
      "source": "citation_dhammapada_2",
      "type": "MENTIONS",
      "target": "concept_citta",
      "source_file": "data/seeds/dhammapada.json"
    },
    {
      "source": "citation_dhammapada_2",
      "type": "MENTIONS",
      "target": "concept_karma",
      "source_file": "data/seeds/dhammapada.json"
    },
    {
      "source": "citation_dhammapada_21",
      "type": "MENTIONS",
      "target": "concept_appamada",
      "source_file": "data/seeds/dhammapada.json"
    },
    {
      "source": "citation_dhammapada_277",
      "type": "MENTIONS",
      "target": "concept_anicca",
      "source_file": "data/seeds/dhammapada.json"
    },
    {
      "source": "citation_dhammapada_279",
      "type": "MENTIONS",
      "target": "concept_anatta",
      "source_file": "data/seeds/dhammapada.json"
    },
    {
      "source": "citation_dhammapada_35",
      "type": "MENTIONS",
      "target": "concept_citta",
      "source_file": "data/seeds/dhammapada.json"
    },
    {
      "source": "citation_dhammapada_5",
      "type": "MENTIONS",
      "target": "concept_metta",
      "source_file": "data/seeds/dhammapada.json"
    },
    {
      "source": "citation_dhammapada_50",
      "type": "MENTIONS",
      "target": "concept_sila",
      "source_file": "data/seeds/dhammapada.json"
    },
    {
      "source": "citation_heart_sutra_dharmas",
      "type": "MENTIONS",
      "target": "concept_ayatana",
      "source_file": "data/seeds/heart_sutra.json"
    },
    {
      "source": "citation_heart_sutra_dharmas",
      "type": "MENTIONS",
      "target": "concept_dhatu",
      "source_file": "data/seeds/heart_sutra.json"
    },
    {
      "source": "citation_heart_sutra_dharmas",
      "type": "MENTIONS",
      "target": "concept_four_noble_truths",
      "source_file": "data/seeds/heart_sutra.json"
    },
    {
      "source": "citation_heart_sutra_dharmas",
      "type": "MENTIONS",
      "target": "concept_pratityasamutpada",
      "source_file": "data/seeds/heart_sutra.json"
    },
    {
      "source": "citation_heart_sutra_mantra",
      "type": "MENTIONS",
      "target": "concept_mantra",
      "source_file": "data/seeds/heart_sutra.json"
    },
    {
      "source": "citation_heart_sutra_mantra",
      "type": "MENTIONS",
      "target": "concept_prajnaparamita",
      "source_file": "data/seeds/heart_sutra.json"
    },
    {
      "source": "citation_heart_sutra_opening",
      "type": "MENTIONS",
      "target": "concept_avalokitesvara",
      "source_file": "data/seeds/heart_sutra.json"
    },
    {
      "source": "citation_heart_sutra_opening",
      "type": "MENTIONS",
      "target": "concept_prajnaparamita",
      "source_file": "data/seeds/heart_sutra.json"
    },
    {
      "source": "citation_heart_sutra_opening",
      "type": "MENTIONS",
      "target": "concept_skandhas",
      "source_file": "data/seeds/heart_sutra.json"
    },
    {
      "source": "citation_heart_sutra_skandhas",
      "type": "MENTIONS",
      "target": "concept_form",
      "source_file": "data/seeds/heart_sutra.json"
    },
    {
      "source": "citation_heart_sutra_skandhas",
      "type": "MENTIONS",
      "target": "concept_skandhas",
      "source_file": "data/seeds/heart_sutra.json"
    },
    {
      "source": "citation_heart_sutra_skandhas",
      "type": "MENTIONS",
      "target": "concept_sunyata",
      "source_file": "data/seeds/heart_sutra.json"
    },
    {
      "source": "citation_mmkv_24_18",
      "type": "MENTIONS",
      "target": "concept_middle_way",
      "source_file": "data/seeds/core.json"
    },
    {
      "source": "citation_mmkv_24_18",
      "type": "MENTIONS",
      "target": "concept_pratityasamutpada",
      "source_file": "data/seeds/core.json"
    },
    {
      "source": "citation_mmkv_24_18",
      "type": "MENTIONS",
      "target": "concept_sunyata",
      "source_file": "data/seeds/core.json"
    },
    {
      "source": "citation_mmkv_24_19",
      "type": "MENTIONS",
      "target": "concept_pratityasamutpada",
      "source_file": "data/seeds/core.json"
    },
    {
      "source": "citation_mmkv_24_19",
      "type": "MENTIONS",
      "target": "concept_sunyata",
      "source_file": "data/seeds/core.json"
    },
    {
      "source": "citation_mmkv_24_19",
      "type": "MENTIONS",
      "target": "concept_two_truths",
      "source_file": "data/seeds/core.json"
    },
    {
      "source": "citation_mmkv_25_19",
      "type": "MENTIONS",
      "target": "concept_nirvana",
      "source_file": "data/seeds/core.json"
    },
    {
      "source": "citation_mmkv_25_19",
      "type": "MENTIONS",
      "target": "concept_samsara",
      "source_file": "data/seeds/core.json"
    },
    {
      "source": "concept_four_noble_truths",
      "type": "MENTIONS",
      "target": "concept_dukkha",
      "source_file": "data/seeds/concepts.json"
    },
    {
      "source": "concept_four_noble_truths",
      "type": "MENTIONS",
      "target": "concept_nirvana",
      "source_file": "data/seeds/concepts.json"
    },
    {
      "source": "concept_four_noble_truths",
      "type": "MENTIONS",
      "target": "concept_noble_eightfold_path",
      "source_file": "data/seeds/concepts.json"
    },
    {
      "source": "concept_four_noble_truths",
      "type": "MENTIONS",
      "target": "concept_tanha",
      "source_file": "data/seeds/concepts.json"
    },
    {
      "source": "concept_noble_eightfold_path",
      "type": "MENTIONS",
      "target": "concept_prajna",
      "source_file": "data/seeds/concepts.json"
    },
    {
      "source": "concept_noble_eightfold_path",
      "type": "MENTIONS",
      "target": "concept_samadhi",
      "source_file": "data/seeds/concepts.json"
    },
    {
      "source": "concept_noble_eightfold_path",
      "type": "MENTIONS",
      "target": "concept_sila",
      "source_file": "data/seeds/concepts.json"
    },
    {
      "source": "text_dhammapada",
      "type": "MENTIONS",
      "target": "concept_anatta",
      "source_file": "data/seeds/dhammapada.json"
    },
    {
      "source": "text_dhammapada",
      "type": "MENTIONS",
      "target": "concept_anicca",
      "source_file": "data/seeds/dhammapada.json"
    },
    {
      "source": "text_dhammapada",
      "type": "MENTIONS",
      "target": "concept_appamada",
      "source_file": "data/seeds/dhammapada.json"
    },
    {
      "source": "text_dhammapada",
      "type": "MENTIONS",
      "target": "concept_citta",
      "source_file": "data/seeds/dhammapada.json"
    },
    {
      "source": "text_dhammapada",
      "type": "MENTIONS",
      "target": "concept_sila",
      "source_file": "data/seeds/dhammapada.json"
    },
    {
      "source": "text_heart_sutra",
      "type": "MENTIONS",
      "target": "concept_avalokitesvara",
      "source_file": "data/seeds/heart_sutra.json"
    },
    {
      "source": "text_heart_sutra",
      "type": "MENTIONS",
      "target": "concept_ayatana",
      "source_file": "data/seeds/heart_sutra.json"
    },
    {
      "source": "text_heart_sutra",
      "type": "MENTIONS",
      "target": "concept_dhatu",
      "source_file": "data/seeds/heart_sutra.json"
    },
    {
      "source": "text_heart_sutra",
      "type": "MENTIONS",
      "target": "concept_prajnaparamita",
      "source_file": "data/seeds/heart_sutra.json"
    },
    {
      "source": "text_heart_sutra",
      "type": "MENTIONS",
      "target": "concept_skandhas",
      "source_file": "data/seeds/heart_sutra.json"
    },
    {
      "source": "text_heart_sutra",
      "type": "MENTIONS",
      "target": "concept_sunyata",
      "source_file": "data/seeds/heart_sutra.json"
    },
    {
      "source": "text_mulamadhyamakakarika",
      "type": "MENTIONS",
      "target": "concept_pratityasamutpada",
      "source_file": "data/seeds/core.json"
    },
    {
      "source": "text_mulamadhyamakakarika",
      "type": "MENTIONS",
      "target": "concept_sunyata",
      "source_file": "data/seeds/core.json"
    },
    {
      "source": "text_mulamadhyamakakarika",
      "type": "MENTIONS",
      "target": "concept_two_truths",
      "source_file": "data/seeds/core.json"
    },
    {
      "source": "concept_avalokitesvara",
      "type": "RELATED_TO",
      "target": "concept_karuna",
      "source_file": "data/seeds/heart_sutra.json"
    },
    {
      "source": "concept_bodhisattva",
      "type": "RELATED_TO",
      "target": "concept_bodhicitta",
      "source_file": "data/seeds/concepts.json"
    },
    {
      "source": "concept_bodhisattva",
      "type": "RELATED_TO",
      "target": "concept_paramita",
      "source_file": "data/seeds/concepts.json"
    },
    {
      "source": "concept_form",
      "type": "RELATED_TO",
      "target": "concept_skandhas",
      "source_file": "data/seeds/heart_sutra.json"
    },
    {
      "source": "concept_four_noble_truths",
      "type": "RELATED_TO",
      "target": "place_sarnath",
      "source_file": "data/seeds/places_traditions.json"
    },
    {
      "source": "concept_klesha",
      "type": "RELATED_TO",
      "target": "concept_avidya",
      "source_file": "data/seeds/concepts.json"
    },
    {
      "source": "concept_klesha",
      "type": "RELATED_TO",
      "target": "concept_tanha",
      "source_file": "data/seeds/concepts.json"
    },
    {
      "source": "concept_middle_way",
      "type": "RELATED_TO",
      "target": "concept_two_truths",
      "source_file": "data/seeds/concepts.json"
    },
    {
      "source": "concept_nirvana",
      "type": "RELATED_TO",
      "target": "place_bodh_gaya",
      "source_file": "data/seeds/places_traditions.json"
    },
    {
      "source": "concept_prajnaparamita",
      "type": "RELATED_TO",
      "target": "concept_paramita",
      "source_file": "data/seeds/heart_sutra.json"
    },
    {
      "source": "concept_prajnaparamita",
      "type": "RELATED_TO",
      "target": "concept_prajna",
      "source_file": "data/seeds/heart_sutra.json"
    },
    {
      "source": "concept_pratityasamutpada",
      "type": "RELATED_TO",
      "target": "concept_avidya",
      "source_file": "data/seeds/concepts.json"
    },
    {
      "source": "concept_pratityasamutpada",
      "type": "RELATED_TO",
      "target": "concept_karma",
      "source_file": "data/seeds/concepts.json"
    },
    {
      "source": "concept_pratityasamutpada",
      "type": "RELATED_TO",
      "target": "concept_tanha",
      "source_file": "data/seeds/concepts.json"
    },
    {
      "source": "concept_samsara",
      "type": "RELATED_TO",
      "target": "concept_avidya",
      "source_file": "data/seeds/concepts.json"
    },
    {
      "source": "concept_samsara",
      "type": "RELATED_TO",
      "target": "concept_karma",
      "source_file": "data/seeds/concepts.json"
    },
    {
      "source": "concept_samsara",
      "type": "RELATED_TO",
      "target": "concept_nirvana",
      "source_file": "data/seeds/concepts.json"
    },
    {
      "source": "concept_sunyata",
      "type": "RELATED_TO",
      "target": "concept_pratityasamutpada",
      "source_file": "data/seeds/concepts.json"
    },
    {
      "source": "concept_sunyata",
      "type": "RELATED_TO",
      "target": "concept_two_truths",
      "source_file": "data/seeds/concepts.json"
    },
    {
      "source": "school_mahayana",
      "type": "RELATED_TO",
      "target": "place_gandhara",
      "source_file": "data/seeds/places_traditions.json"
    },
    {
      "source": "school_pali_canon",
      "type": "RELATED_TO",
      "target": "school_theravada",
      "source_file": "data/seeds/places_traditions.json"
    },
    {
      "source": "term_anatta_pali",
      "type": "RELATED_TO",
      "target": "term_anatman_sanskrit",
      "source_file": "data/seeds/terms.json"
    },
    {
      "source": "term_anicca_pali",
      "type": "RELATED_TO",
      "target": "term_anitya_sanskrit",
      "source_file": "data/seeds/terms.json"
    },
    {
      "source": "term_avijja_pali",
      "type": "RELATED_TO",
      "target": "term_avidya_sanskrit",
      "source_file": "data/seeds/terms_extended.json"
    },
    {
      "source": "term_dukkha_pali",
      "type": "RELATED_TO",
      "target": "term_duhkha_sanskrit",
      "source_file": "data/seeds/terms.json"
    },
    {
      "source": "term_kamma_pali",
      "type": "RELATED_TO",
      "target": "term_karma_sanskrit",
      "source_file": "data/seeds/terms_extended.json"
    },
    {
      "source": "term_nibbana_pali",
      "type": "RELATED_TO",
      "target": "term_nirvana_sanskrit",
      "source_file": "data/seeds/terms.json"
    },
    {
      "source": "term_panna_pali",
      "type": "RELATED_TO",
      "target": "term_prajna_sanskrit",
      "source_file": "data/seeds/terms_extended.json"
    },
    {
      "source": "term_paticcasamuppada_pali",
      "type": "RELATED_TO",
      "target": "term_pratityasamutpada_sanskrit",
      "source_file": "data/seeds/terms.json"
    },
    {
      "source": "term_tanha_pali",
      "type": "RELATED_TO",
      "target": "term_trsna_sanskrit",
      "source_file": "data/seeds/terms_extended.json"
    }
  ]
};
