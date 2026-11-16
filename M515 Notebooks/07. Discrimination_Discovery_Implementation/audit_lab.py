# 1. Load the applicant records
from pathlib import Path  # Locate the data and results beside this script.
import pandas as pd  # Work with readable tables.
import matplotlib  # Use a graphics backend that can save files without a window.

matplotlib.use("Agg")  # Run on a laptop, server, or terminal without a display.
root = Path(__file__).resolve().parent  # Find the extracted lab folder.
data_file = root / "data" / "applicants_16.csv"  # Locate the same 16 records as the notebook.
applicants = pd.read_csv(data_file)  # Load one row per applicant.
print(applicants.to_string(index=False))  # Show the source inputs.

# 2. Make the original screening decisions
audit = applicants.copy()  # Keep the source records intact.
audit["screen_score"] = audit["skill"] + 10 * audit["has_car"]  # Add the original car bonus.
audit["invited"] = audit["screen_score"] >= 70  # True means an invitation.
audit["denied"] = ~audit["invited"]  # True means no invitation.
fields = ["applicant", "skill", "has_car", "screen_score", "invited"]  # Pick columns for the trace.
pair = audit["applicant"].isin(["W01", "M01"])  # Mark the two records.
print(audit.loc[pair, fields].to_string(index=False))  # Check the hand calculation.

# 3. Count access by group
by_group = audit.groupby("group", sort=False)  # Keep one set of rows for each audit group.
invited_count = by_group["invited"].sum()  # True counts as 1; False counts as 0.
applicant_count = by_group.size()  # Count both invited and denied applicants.
invitation_rate = invited_count / applicant_count  # Use all applicants in each group.
access = pd.DataFrame()  # Build the result one visible column at a time.
access["invited"] = invited_count  # Numerator.
access["applicants"] = applicant_count  # Denominator.
access["invitation_rate"] = invitation_rate  # Result.
print(access.to_string())  # Compare counts and rates side by side.
access_gap = invitation_rate["Women"] - invitation_rate["Men"]  # Use a fixed subtraction order.
print(f"Invitation gap (Women − Men): {100 * access_gap:+.1f} pp")  # Express the difference in percentage points.

# 4. Compute the subgroup rule metrics
junior = audit["experience"] == "0–2 years"  # Mark the context.
women = audit["group"] == "Women"  # Mark the audit group.
rule_rows = audit[junior & women]  # Antecedent: both conditions must be true.
rule_denied = rule_rows["denied"].sum()  # Count denials inside that antecedent.
support = rule_denied / len(audit)  # Denominator: all 16 records.
confidence = rule_denied / len(rule_rows)  # Denominator: the 4 matching records.
context_rate = audit.loc[junior, "denied"].mean()  # Mean of True/False gives 4/8 here.
extended_lift = confidence / context_rate  # Compare the two rates; the context rate is nonzero.
print(f"Support: {support:.2%}; confidence: {confidence:.0%}; extended lift: {extended_lift:.2f}")  # Check the arithmetic.

# 5. Check both experience bands
for band in ["0–2 years", "3+ years"]:  # Look at two named contexts only.
    context = audit[audit["experience"] == band]  # Filter to the current context.
    counts = context.groupby("group", sort=False)["denied"].agg(["sum", "size"])  # Count denials and people.
    counts = counts.rename(columns={"sum": "denials", "size": "applicants"})  # Label both counts.
    counts["denial_rate"] = counts["denials"] / counts["applicants"]  # Divide by the matching group count.
    print(f"Experience: {band}")  # Tell readers which subset is shown.
    print(counts.to_string())  # Show both groups including the smaller or zero-denial cells.

# 6. Count missed qualified applicants
qualified = audit["qualifies"] == 1  # Select reference-positive applicants.
missed = audit["denied"] & qualified  # Both conditions are needed for a false negative.
audit["missed_qualified"] = missed  # Save the row-level error for inspection.
missed_counts = audit.groupby("group", sort=False)["missed_qualified"].sum()  # False negatives by group.
qualified_counts = audit.groupby("group", sort=False)["qualifies"].sum()  # Count reference positives.
fnr = missed_counts / qualified_counts  # Both groups have qualified records in this example.
errors = pd.DataFrame()  # Build an error table for the two groups.
errors["false_negatives"] = missed_counts  # Numerator.
errors["qualified"] = qualified_counts  # Denominator.
errors["fnr"] = fnr.round(3)  # Round only for display.
print(errors.to_string())  # Show counts and rates.
print("Missed qualified applicants:", audit.loc[missed, "applicant"].tolist())  # Trace the burden to people.

# 7. Isolate the effect of car ownership
fixed_skill = 68  # Hold W01's skill constant.
for car in [0, 1]:  # Vary only ownership in the rule.
    score = fixed_skill + 10 * car  # Apply the exact original formula.
    invited = score >= 70  # Translate the score into a decision.
    print(f"has_car={car}: score={score}, invited={invited}")  # See what actually changes.

# 8. Compare three fixed policies
audit["skill_at_70"] = audit["skill"] >= 70  # Change the feature, keep the threshold.
audit["skill_at_65"] = audit["skill"] >= 65  # Change the threshold on the skill-only score.
policies = ["invited", "skill_at_70", "skill_at_65"]  # Compare three explicit alternatives.
policy_names = ["Original: 70", "No bonus: 70", "No bonus: 65"]  # Names for the table and plot.
policy_rows = []  # Collect one row for each policy.

for name, policy in zip(policy_names, policies):  # Pair display names with columns.
    decision = audit[policy]  # True means invited under the current policy.
    corrected = decision == qualified  # Check agreement with the reference for each person.
    new_misses = (~decision) & qualified  # Qualified people still denied.
    extra_invites = decision & (~qualified)  # Invitations without a positive reference.
    women_invited = decision[women].sum()  # Invited women out of 8 in this cohort.
    men_invited = decision[~women].sum()  # Invited men out of 8 in this two-group cohort.
    policy_rows.append([name, women_invited, men_invited, corrected.sum(),  # Keep counts.
                        new_misses.sum(), extra_invites.sum()])  # Add both error types.
columns = ["Policy", "W invited / 8", "M invited / 8", "Correct / 16", "FN", "FP"]  # Label counts.
comparison = pd.DataFrame(policy_rows, columns=columns)  # Turn the rows into a table.
print(comparison.to_string(index=False))  # Compare all three policies.

# 9. Trace who gains and loses access
for alternative in ["skill_at_70", "skill_at_65"]:  # Compare each change with the original rule.
    gained = audit[alternative] & (~audit["invited"])  # Now invited, previously denied.
    lost = (~audit[alternative]) & audit["invited"]  # Now denied, previously invited.
    print(f"{alternative} — gains:", audit.loc[gained, "applicant"].tolist())  # Show who gains access.
    print(f"{alternative} — losses:", audit.loc[lost, "applicant"].tolist())  # Show who loses access.

# 10. Plot and save results
import matplotlib.pyplot as plt  # Make one comparison plot.

rates = audit.groupby("group", sort=False)[policies].mean().T * 100  # Convert rates to percent.
rates.index = policy_names  # Give the rows plain names.
misses = comparison.set_index("Policy")["FN"]  # Use the false negatives already counted.
fig, axes = plt.subplots(1, 2, figsize=(10, 3.7))  # Put outcomes and errors side by side.
rates.plot.bar(ax=axes[0], color=["#173459", "#218784"], rot=0)  # Compare invitation rates.
axes[0].set(title="Who was invited?", ylabel="Invited (%)", ylim=(0, 110))  # Show the scale.
axes[0].legend(loc="upper left", ncols=2)  # Identify the groups.
misses.plot.bar(ax=axes[1], color="#B75547", rot=0)  # Plot the missed qualified applicants.
axes[1].bar_label(axes[1].containers[0], padding=4)  # Label all three counts, including zero.
axes[1].set(title="Who was wrongly denied?", ylabel="Qualified applicants missed",  # Name error.
            ylim=(0, 5), xlabel="", yticks=range(6))  # Count people on an integer scale.
fig.tight_layout()  # Leave room for text.

results = root / "results"  # Keep outputs separate from the source data.
results.mkdir(exist_ok=True)  # Create the results folder on the first run.
fig.savefig(results / "policy_comparison.png", dpi=140)  # Save the figure shown in the notebook.
audit.to_csv(results / "applicant_audit.csv", index=False)  # Save row-level decisions.
comparison.to_csv(results / "policy_comparison.csv", index=False)  # Save policy totals.
print(f"Results saved in {results}")  # Show where the files went.
