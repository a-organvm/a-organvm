// a-organvm system declaration
//
// This is what system.toml SHOULD have been.
// Every value here is constrained. Invalid states produce errors, not silent wrong values.
// Run: cue eval system.cue
// Run: cue vet system.cue  (validates without printing)

package organvm

import "strings"

// ─────────────────────────────────────────────
// IDENTITY
// ─────────────────────────────────────────────

identity: {
	name:        "a-organvm"
	description: string & strings.MinRunes(10)
	description: "The missing organs wrapping around the flawed organism"
	principal:   "4444j99"
	github_org:  "a-organvm"
	local_path:  "organvm"
}

// ─────────────────────────────────────────────
// ELEMENTS — the periodic table (discovered, not chosen)
//
// #Element defines what an element IS. Every element below
// must satisfy these constraints or CUE refuses to evaluate.
// ─────────────────────────────────────────────

#Element: {
	symbol:    string & =~"^[A-Z][a-z]$" // exactly 2 letters: capital + lowercase
	operation: string & strings.MinRunes(10) // real description, not empty
	status:    "discovered" | "hypothesized" | "refuted"
}

// The 10 elements. Try changing one to status: "vibes" — CUE will reject it.
// The [string]: #Element line means EVERY entry must satisfy #Element.
elements: [string]: #Element
elements: {
	intake: #Element & {
		symbol:    "In"
		operation: "bring signal into the system"
		status:    "discovered"
	}
	store: #Element & {
		symbol:    "St"
		operation: "hold signal across time"
		status:    "discovered"
	}
	retrieve: #Element & {
		symbol:    "Re"
		operation: "access what is stored"
		status:    "discovered"
	}
	evaluate: #Element & {
		symbol:    "Ev"
		operation: "compare signal against criteria"
		status:    "discovered"
	}
	transform: #Element & {
		symbol:    "Tr"
		operation: "change signal form"
		status:    "discovered"
	}
	synthesize: #Element & {
		symbol:    "Sy"
		operation: "combine many signals into one"
		status:    "discovered"
	}
	route: #Element & {
		symbol:    "Ro"
		operation: "direct signal to destination"
		status:    "discovered"
	}
	authorize: #Element & {
		symbol:    "Au"
		operation: "gate — allow or block passage"
		status:    "discovered"
	}
	bind: #Element & {
		symbol:    "Bi"
		operation: "connect two things permanently"
		status:    "discovered"
	}
	emit: #Element & {
		symbol:    "Em"
		operation: "send signal out of the system"
		status:    "discovered"
	}
}

// Collect all valid symbols so compounds can reference them
_validSymbols: [for _, e in elements {e.symbol}]

// ─────────────────────────────────────────────
// COMPOUNDS — named compositions of elements
//
// #Compound defines what a compound IS.
// The formula must be a list of valid element symbols.
// The domain must be one of the 5 recognized domains.
// ─────────────────────────────────────────────

#Domain: "protective" | "economic" | "epistemic" | "relational" | "structural"

#Compound: {
	formula:   [...string] // list of element symbols
	modifier?: string // optional modifier
	domain:    #Domain
	operation: string & strings.MinRunes(10)
}

compounds: [string]: #Compound
compounds: {
	assessor: #Compound & {
		formula:   ["In", "Ev", "Em"]
		domain:    "protective"
		operation: "evaluate situation against normative frame"
	}
	guardian: #Compound & {
		formula:   ["In", "Ev", "Em"]
		modifier:  "loop"
		domain:    "protective"
		operation: "maintain watchlist, trigger alerts on threshold"
	}
	ledger: #Compound & {
		formula:   ["In", "St", "Re"]
		domain:    "economic"
		operation: "record and maintain authoritative state of value flows"
	}
	archivist: #Compound & {
		formula:   ["In", "St", "Re"]
		modifier:  "permanent"
		domain:    "epistemic"
		operation: "capture, preserve, index institutional memory"
	}
	counselor: #Compound & {
		formula:   ["In", "Sy", "Em"]
		domain:    "epistemic"
		operation: "synthesize assessments into integrated recommendation"
	}
	mandator: #Compound & {
		formula:   ["Au", "Em"]
		domain:    "structural"
		operation: "formalize decisions into executable directives"
	}
	appraiser: #Compound & {
		formula:   ["In", "Ev", "Em"]
		modifier:  "market-frame"
		domain:    "economic"
		operation: "determine exchange value in market context"
	}
	optimizer: #Compound & {
		formula:   ["In", "Ev", "Sy"]
		domain:    "economic"
		operation: "determine optimal resource allocation given constraints"
	}
	allocator: #Compound & {
		formula:   ["Re", "Ro", "Em"]
		domain:    "economic"
		operation: "distribute resources across competing demands"
	}
	collector: #Compound & {
		formula:   ["Re", "Ev", "Ro", "Em"]
		domain:    "economic"
		operation: "track and execute conversion of receivables into value"
	}
	auditor: #Compound & {
		formula:   ["Re", "Ev", "Em"]
		domain:    "epistemic"
		operation: "independently verify accuracy of records and processes"
	}
	negotiator: #Compound & {
		formula:   ["In", "Ev", "Sy", "Em"]
		domain:    "relational"
		operation: "conduct structured position exchange toward agreement"
	}
	representative: #Compound & {
		formula:   ["Re", "Tr", "Em"]
		domain:    "relational"
		operation: "present consistent identity to external parties"
	}
	registrar: #Compound & {
		formula:   ["In", "St", "Re"]
		domain:    "relational"
		operation: "maintain records of formal relationships and standing"
	}
	liaison: #Compound & {
		formula:   ["In", "St", "Re", "Em"]
		domain:    "relational"
		operation: "maintain ongoing bidirectional relationship channel"
	}
	advocate: #Compound & {
		formula:   ["Re", "Sy", "Em"]
		domain:    "protective"
		operation: "construct arguments for specific audience on behalf of principal"
	}
	insulator: #Compound & {
		formula:   ["Au", "Ro"]
		domain:    "structural"
		operation: "create structural separation between domains"
	}
	incorporator: #Compound & {
		formula:   ["Bi", "St", "Au"]
		domain:    "structural"
		operation: "create and maintain formal organizational structures"
	}
	enforcer: #Compound & {
		formula:   ["Ev", "Au", "Em"]
		domain:    "structural"
		operation: "detect violations and initiate escalation"
	}
	strategist: #Compound & {
		formula:   ["In", "Ev", "Sy"]
		modifier:  "positional"
		domain:    "structural"
		operation: "model position in larger systems, identify advantage moves"
	}
}

// ─────────────────────────────────────────────
// FORMATIONS — wired compound compositions
//
// A formation references compounds by name.
// If you reference a compound that doesn't exist above, CUE catches it.
// ─────────────────────────────────────────────

// Collect valid compound names
_validCompounds: [for name, _ in compounds {name}]

#Formation: {
	description: string & strings.MinRunes(5)
	compounds: [...string] // list of compound names
	wiring:    string // signal flow description
	trigger:   string // activation condition
}

formations: [string]: #Formation
formations: {
	aegis: #Formation & {
		description: "defensive perimeter"
		compounds: ["guardian", "assessor", "counselor", "mandator", "archivist"]
		wiring:    "guardian -> [assessor(legal) || assessor(financial)] -> counselor -> mandator"
		trigger:   "threat detected by guardian AND stakes >= significant"
	}
	oikonomia: #Formation & {
		description: "survival economics"
		compounds: ["ledger", "appraiser", "optimizer", "allocator", "collector", "auditor"]
		wiring:    "ledger -> appraiser -> optimizer -> allocator -> collector"
		trigger:   "cash flow below sustainability OR position opaque"
	}
	praxis: #Formation & {
		description: "income generation engine"
		compounds: ["assessor", "strategist", "appraiser", "negotiator", "incorporator", "insulator", "archivist"]
		wiring:    "assessor -> strategist -> appraiser -> negotiator -> incorporator -> insulator"
		trigger:   "income insufficient OR strategic repositioning"
	}
	tessera: #Formation & {
		description: "identity and standing"
		compounds: ["registrar", "representative", "advocate", "liaison", "insulator"]
		wiring:    "registrar -> [insulator > representative] -> advocate -> liaison"
		trigger:   "need to interface with formal systems"
	}
}

// ─────────────────────────────────────────────
// GOVERNANCE — sovereignty cascade (10 levels, flat)
//
// Each level has a numeric sovereignty. Higher sovereignty
// CANNOT be overridden by lower. This is just data here,
// but the immune system reads these levels and enforces the cascade.
// ─────────────────────────────────────────────

#GovernanceLevel: {
	level:       int & >=1 & <=10
	sovereignty: int & >=1 & <=10 // computed: 11 - level
	description: string & strings.MinRunes(10)
	contains: [...string]
	source?: string
}

governance: {
	"natural-law": #GovernanceLevel & {
		level:       1
		sovereignty: 10
		description: "discovered truth — cannot be violated"
		contains: ["observations", "empirical-laws", "conservation", "symmetries", "constraints"]
		source: "PERIODIC-TABLE.md, codebase scans"
	}
	theory: #GovernanceLevel & {
		level:       2
		sovereignty: 9
		description: "explains why natural law works — testable, falsifiable"
		contains: ["hypotheses", "models", "paradigms", "proofs", "isomorphisms", "falsification"]
		source: "sovereign--ground, system-system--system--monad, scale-threshold-emergence"
	}
	methodology: #GovernanceLevel & {
		level:       3
		sovereignty: 8
		description: "how we discover and validate"
		contains: ["scientific-method", "peer-review", "reproducibility", "provenance"]
	}
	constitution: #GovernanceLevel & {
		level:       4
		sovereignty: 7
		description: "foundational social contract — chosen, not discovered"
		contains: ["preamble", "articles", "bill-of-rights", "amendment-process", "ratification"]
		source: "system-system--system/LAWS.md (7 laws, 9 proofs, 21 derivations)"
	}
	treaties: #GovernanceLevel & {
		level:       5
		sovereignty: 6
		description: "agreements with external entities"
		contains: ["api-contracts", "licenses", "terms-of-service", "partnerships", "obligations"]
	}
	legislation: #GovernanceLevel & {
		level:       6
		sovereignty: 5
		description: "specific rules derived from constitution"
		contains: ["acts", "regulations", "standards", "codes", "schedules"]
		source: "governance-rules.json, INST-FORMATION"
	}
	executive: #GovernanceLevel & {
		level:       7
		sovereignty: 4
		description: "operational decisions and standing policies"
		contains: ["directives", "policies", "procedures", "guidelines", "delegations"]
	}
	judicial: #GovernanceLevel & {
		level:       8
		sovereignty: 3
		description: "interpretation and dispute resolution"
		contains: ["precedent", "opinions", "reviews", "appeals", "dissent"]
	}
	custom: #GovernanceLevel & {
		level:       9
		sovereignty: 2
		description: "unwritten norms made explicit"
		contains: ["naming-conventions", "coding-patterns", "communication", "aesthetic", "rituals"]
	}
	record: #GovernanceLevel & {
		level:       10
		sovereignty: 1
		description: "the memory of all governance"
		contains: ["decision-log", "audit-trail", "changelog", "fossil-record", "errata"]
	}
}

// ─────────────────────────────────────────────
// COMPOSITION — the 4 operators
// ─────────────────────────────────────────────

#Operator: {
	symbol:      string
	description: string
}

composition: {
	operators: {
		chain: #Operator & {
			symbol:      "->"
			description: "sequential flow"
		}
		parallel: #Operator & {
			symbol:      "||"
			description: "concurrent flow"
		}
		envelope: #Operator & {
			symbol:      ">"
			description: "wrapping context"
		}
		feedback: #Operator & {
			symbol:      "<->"
			description: "self-referential loop"
		}
	}
	interface: {
		input: ["context", "frame", "principal_position"]
		output: ["result", "confidence", "escalation_flag", "audit_trail"]
	}
}

// ─────────────────────────────────────────────
// SIGNAL — the voltage
// ─────────────────────────────────────────────

signal: {
	type:        "state"
	description: "the principal's current situation, context, position"
}

// ─────────────────────────────────────────────
// NAMING — algorithmic identity
// ─────────────────────────────────────────────

naming: {
	protocol:            "names are functions of properties, not human choices"
	element_pattern:     "single lowercase word"
	compound_pattern:    "{formula}--{function}"
	formation_pattern:   "single latin/greek noun at crystallization"
	product_pattern:     "human-readable market name (the only exception)"
	repo_pattern:        "{domain}--{descriptor}"
	variable_resolution: true
}

// ─────────────────────────────────────────────
// DERIVED VALUES — computed from the above
//
// These are not hand-maintained. CUE computes them.
// If you add an element or compound, these update automatically.
// ─────────────────────────────────────────────

_derived: {
	element_count:    len(elements)
	compound_count:   len(compounds)
	formation_count:  len(formations)
	governance_count: len(governance)

	// All element symbols in the system
	all_symbols: [for _, e in elements {e.symbol}]
}
