# Team Setup Guide

How to customize enggenie for your team. All configuration goes in your project's `CLAUDE.md` or in specific file locations within your repo. No forking required.

## Spec Template Override

By default, pm-refine uses the template at `templates/spec-template.md` in the enggenie plugin. To use your team's own format, place a template at either of these locations in your repo:

```
docs/enggenie/templates/spec-template.md    (preferred)
templates/spec-template.md                   (fallback)
```

The skill checks for a team template first. If none is found, it falls back to the default.

Your template should include section headers matching your team's spec format. The skill fills in the content; the template provides the structure. See the default template for reference on what sections to include.

## Commit Format Configuration

deploy-ship uses conventional commits by default. Teams can customize the format by adding a configuration block to their project's `CLAUDE.md`:

```markdown
## Commit Conventions
- emoji_prefix: true
- jira_in_subject: true
- conventional_commits_strict: true
- co_authored_by: true
```

### Available Options

| Setting | Effect | Default | Example |
|---------|--------|---------|---------|
| `emoji_prefix` | Adds emoji before commit type | Off | `feat: add search` |
| `jira_in_subject` | Adds Jira ticket to subject line | Off | `[PROJ-1234] feat: add search` |
| `conventional_commits_strict` | Rejects non-conforming messages | Off | Enforces `type: description` format |
| `co_authored_by` | Adds co-author tag | Off | `Co-authored-by: AI Assistant <team@example.com>` |

You can enable any combination. The skill reads these settings and applies them to the commit message proposal. The user still confirms before anything is committed.

## Estimation Method Configuration

pm-refine defaults to Fibonacci estimation (1, 2, 3, 5, 8) with an 8-point cap. To change the method, add to your `CLAUDE.md`:

```markdown
## Estimation Method
fibonacci
```

### Available Methods

**Fibonacci (default):**
```markdown
## Estimation Method
fibonacci
```
Scale: 1, 2, 3, 5, 8. Raw estimate + 20% buffer, rounded up to the nearest Fibonacci number. Stories above 8 points must be decomposed.

**T-shirt sizing:**
```markdown
## Estimation Method
t-shirt
```
Scale: XS, S, M, L, XL. Mapped internally to 1, 2, 3, 5, 8 for calculation. Displayed as T-shirt sizes in output.

**Linear:**
```markdown
## Estimation Method
linear
```
Scale: 1-10. Raw estimate + 20% buffer, no Fibonacci rounding. Stories above 8 are still flagged for decomposition.

## Architecture Context

Describe your system topology in `CLAUDE.md` so skills understand your architecture without re-discovering it each session. This context is used by pm-refine (Architecture Context section of specs), architect-design (system mapping), and architect-plan (codebase discovery).

```markdown
## Architecture Context

Monorepo with three services:

- **api-gateway** (Node.js/Express) - Routes requests, handles auth
- **billing-service** (C#/.NET) - Invoice generation, payment processing
- **notification-service** (Python/FastAPI) - Email, SMS, push notifications

Shared:
- PostgreSQL (billing-service owns schema)
- RabbitMQ for async messaging between services
- Redis for session cache (api-gateway)

Deployment: Docker containers on AWS ECS, deployed via GitHub Actions.
```

Be specific. Name the services, frameworks, databases, and messaging systems. The more concrete the context, the better the specs, plans, and implementations.

## Jira Project Key

If your team uses Jira, configure the project key so pm-refine and deploy-ship can create and update tickets automatically:

```markdown
## Jira
- project_key: PROJ
```

When configured, pm-refine will create story and subtask tickets in the specified project. deploy-ship will transition ticket status and add PR links as comments.

If Jira MCP tools are not available, both skills degrade gracefully -- they output the ticket structure in text for manual creation and mention the ticket update needed.

## Full Example CLAUDE.md

Here is a complete example combining all configuration options:

```markdown
# Project Configuration

## Architecture Context

React frontend with .NET API backend.

- **web-app** (React/TypeScript) - SPA, Vite build, deployed to CloudFront
- **api** (C#/.NET 8) - REST API, Entity Framework, deployed to ECS
- **worker** (C#/.NET 8) - Background job processor, SQS consumer

Database: PostgreSQL on RDS.
Cache: Redis on ElastiCache.
Auth: Cognito with JWT tokens.

## Commit Conventions
- jira_in_subject: true
- conventional_commits_strict: true

## Estimation Method
fibonacci

## Jira
- project_key: PLAT
```

## What Each Skill Reads

| Setting | Used By |
|---------|---------|
| Spec template | pm-refine |
| Commit conventions | deploy-ship |
| Estimation method | pm-refine |
| Architecture context | pm-refine, architect-design, architect-plan |
| Jira project key | pm-refine, deploy-ship |

## Custom Skills

If your team needs domain-specific skills (e.g., a skill for your internal deployment tool or a specific compliance workflow), create them in your team's own plugin -- not in enggenie core. See [Writing Custom Skills](writing-custom-skills.md) for how to extend the suite.
