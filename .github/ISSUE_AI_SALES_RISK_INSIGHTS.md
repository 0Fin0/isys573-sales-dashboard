# Add AI Sales Risk Insights panel to the dashboard

## Business Need

Sales managers can see charts and KPIs, but they still need to interpret which
metrics require attention. Add a dashboard panel called **AI Sales Risk
Insights** that translates existing sales data into a short, evidence-based
summary of business risks and recommended next actions.

This should be implemented as a dashboard feature, not as a call to an external
AI API. The goal is to simulate responsible AI-assisted analysis using
transparent business rules grounded in the dashboard data.

## Requested Feature

Add a visible **AI Sales Risk Insights** panel to the main dashboard experience.

The panel should show at least three insights. Each insight should include:

- A short risk or opportunity title.
- The evidence from the dashboard data that supports it.
- A recommended business action.
- A confidence or priority label such as High, Medium, or Low.

Example insight categories:

- Revenue concentration risk.
- Low-performing product or region.
- Pipeline or conversion risk.
- Strong performance opportunity worth expanding.

## Responsible AI Requirements

- Do not add API keys, tokens, or calls to external AI services.
- Do not invent data or unsupported claims.
- Ground every insight in data already available to the app.
- Add a small note near the panel that says the insights are generated from
  dashboard data and should be reviewed by a human before action.
- Use professional, non-discriminatory language.
- Handle missing or empty data gracefully.

## Acceptance Criteria

- The dashboard includes an **AI Sales Risk Insights** panel on the main view.
- The panel displays at least three data-grounded insights.
- Each insight includes evidence and a suggested action.
- The feature follows existing UI style and remains readable on desktop and
  mobile widths.
- Existing dashboard behavior still works.
- No secrets or external AI service calls are added.
- Existing tests/build checks pass, or manual verification is documented if the
  project has no test suite.
- The pull request summary explains the business value, files changed, testing
  performed, and limitations.

## Assignment

Please implement this issue with GitHub Copilot coding agent and open a draft
pull request for human review.
