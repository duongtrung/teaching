# Fair access to information: calculations and ethical decisions

Matching deck: 03. Fair_Access_to_Information.pptx. One fictional case matches one notebook.

Unzip the whole folder. Install requirements and open notebooks/01_fair_information_access.ipynb. Run the setup first. Part 1 explains the data, calculations and ethical issues. Part 2 offers final-project hints and TODOs. TODO functions raise only when called.

The cohort has twelve eligible students, six residents R1–R6 and six commuters C1–C6. Staff are outside the graph. Two is the initial briefing budget. Eight or eleven is an example informed count. Registration and attendance require separate data. A three-briefing plan reaches all twelve by round 2 under p=1.

The general problem is the institution's allocation of useful information that gives access to an opportunity or a response to a risk. Section 13 explains the ethical issues through individual gains and losses, real settings, an access-check dataset and a worked decision memo. Scholarship and employer-training scenarios are illustrative. BBK warning channels and OECD's discussion of benefit access provide documented real-world connections. W3C supplies an accessibility reference.

All people, housing labels, links and access-check conditions are fictional. The network makes no empirical claim about commuter or resident friendships or needs. The new access checks do not infer individual needs from housing, constitute an accessibility certification or describe any real students.

data/raw retains people.csv, links.csv and node_positions.json. New access_checks.csv supplies the fictional conditions and their provenance. data/processed contains traces, policy comparisons, all 66 pairs, simulations, individual access changes and a receipt-versus-usable-access audit. src/network_lab.py contains the original simulator. Seeds count at round 0. Each link gets one attempt and each student counts once. Greedy ties follow raw class-list row order.

150-minute route: 0–15 setup; 15–35 hand calculations; 35–55 generalization and ethical discussion; 55–65 checkpoint and policy rule; 65–75 break; 75–85 deadline; 85–125 guided practice; 125–140 inclusion and project direction; 140–150 ethical recommendation. Core notebook sections are 1–8 and 11–13. Sections 9–10 are optional methods for self-study.

All 18 code cells executed in a fresh in-process IPython session. The notebook includes eight figures. Jupyter server startup was not tested. Project TODOs remain intentionally incomplete. See SLIDE_GUIDE.md for slide mapping and the Section 13 assessment task.
