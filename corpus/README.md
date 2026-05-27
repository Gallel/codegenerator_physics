# Evaluation corpus

Physics problems used to evaluate the ontology-driven DSL pipeline. 
Each problem lives in its own folder (`problem_XXX/`) with four files:


- `description.txt` — the natural-language statement fed to the LLM.
- `metadata.json` — domain, difficulty, source, URL, format adaptations.
- `expected_goals.json` — the quantities the program must compute.
- `reference_solution.json` — the official numeric answers (with units).

## Inclusion criteria

Problems were curated from official Spanish university-entrance exams 
(PAU / EBAU / EvAU / EAU, 2022-2025). A problem was included only if:


1. It is solvable entirely within the ontology domain: linear and angular 
kinematics, free fall, dynamics (without friction or inclined planes), 
work and energy, fluid statics, and orbital gravitation.
2. It has an official, verifiable numeric solution.
3. Every goal is a numeric value (qualitative sub-questions were removed).

Only the *format* of the statements was adapted (translation to English, 
compaction, removal of qualitative sub-questions). The physics, the numeric 
data and the problem structure were never modified. Each adaptation is 
documented in the `format_adaptations` field of every `metadata.json`.

## Distribution

**By domain:** angular_kinematics (3), dynamics (3), fluid_statics (3), free_fall (2), gravitation (7), linear_kinematics (4), work_energy (5).

**By difficulty:** medium (12), easy (13), hard (2).

## Index

| ID | Domain | Difficulty | Source |
|---|---|---|---|
| problem_001 | gravitation | medium | Aragón |
| problem_002 | gravitation | medium | Aragón |
| problem_003 | gravitation | medium | Aragón |
| problem_004 | gravitation | medium | Catalunya |
| problem_005 | gravitation | medium | Catalunya |
| problem_006 | gravitation | medium | Catalunya |
| problem_007 | gravitation | medium | Castilla-La Mancha |
| problem_008 | linear_kinematics | easy | Castilla-La Mancha |
| problem_009 | linear_kinematics | easy | Castilla-La Mancha |
| problem_010 | linear_kinematics | easy | Cantabria |
| problem_011 | linear_kinematics | easy | Cantabria |
| problem_012 | free_fall | easy | Castilla-La Mancha |
| problem_013 | free_fall | easy | Castilla-La Mancha |
| problem_014 | angular_kinematics | easy | Castilla-La Mancha |
| problem_015 | angular_kinematics | medium | Cantabria |
| problem_016 | angular_kinematics | medium | Castilla-La Mancha |
| problem_017 | dynamics | medium | País Vasco / Universidad del País Vasco (EHU) |
| problem_018 | work_energy | medium | Castilla-La Mancha |
| problem_019 | work_energy | easy | Castilla-La Mancha |
| problem_020 | work_energy | medium | Castilla-La Mancha |
| problem_021 | work_energy | easy | País Vasco / Universidad del País Vasco (EHU) |
| problem_022 | work_energy | easy | País Vasco / Universidad del País Vasco (EHU) |
| problem_023 | fluid_statics | hard | Asturias / Universidad de Oviedo |
| problem_024 | dynamics | hard | UNED |
| problem_025 | dynamics | easy | UNED |
| problem_026 | fluid_statics | easy | Extremadura |
| problem_027 | fluid_statics | easy | Andalucía / Universidad de Cádiz |
