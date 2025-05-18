
def socratic_prompt(decision_summary):
    return f"""
A procurement manager submitted the following decision rationale: 
"{decision_summary}"

As an AI trained to support critical thinking, generate 3-5 Socratic-style questions 
that challenge assumptions and encourage deeper reflection on this decision.
"""

def bias_prompt(decision_text):
    return f"""
Here is a procurement decision rationale: "{decision_text}"

Identify any signs of cognitive bias, such as confirmation bias, sunk cost fallacy,
status quo bias, or availability bias. Provide specific reasoning.
"""
