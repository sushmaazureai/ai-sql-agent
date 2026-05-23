✅ DBA Backup, Restore & Refresh Knowledge Base
(FINAL – VERSION 8.0 – EXECUTION READY)
---
METADATA
Platform: SQL Server DBA Operations
Default Backup Location: C:\SQLBackups
Version: 8.0 (Agent Execution Ready)
Last Updated: 07-Apr-2026
---
=========================================================
SECTION 1: PURPOSE
=========================================================
This document defines the authoritative, execution-ready operational standard
for performing:
BACKUP
RESTORE (NEW)
REFRESH (OVERWRITE)
Designed for:
✔ AI Agents
✔ Automation Pipelines
✔ Manual DBA Execution
---
=========================================================
SECTION 2: OPERATION TYPES
=========================================================
BACKUP
NEW_RESTORE
REFRESH
---
=========================================================
SECTION 3: MANDATORY INPUTS (STRICT VALIDATION)
=========================================================
REQUIRED INPUTS
Source Host
Target Host (for restore/refresh)
Database Name
Operation Type
VALIDATION RULE
IF any input is missing →
❌ STOP EXECUTION
❌ Prompt user again
---
=========================================================
SECTION 4: ENVIRONMENT SAFETY
=========================================================
ENVIRONMENT TAG (MANDATORY)
PROD
NON_PROD
RULES
IF ENV = PROD:
Require DOUBLE APPROVAL
Block overwrite unless explicitly confirmed
IF ENV = NON_PROD:
Single approval sufficient
---
=========================================================
SECTION 5: APPROVAL MODEL
=========================================================
USER APPROVAL REQUIRED
Accepted responses:
YES
APPROVE
PROCEED
TOKEN VALIDATION
APPROVAL_TOKEN must match system value.
IF token invalid →
❌ STOP EXECUTION
---
=========================================================
SECTION 6: PERMISSIONS HANDLING
=========================================================
STEP 1: CAPTURE RIGHTS
Tool:
execute_sp(hostname, "msdb", "EXEC dbo.rfrsh_copyrights_output", "")
Expected:
✔ Permissions captured count
On Failure:
❌ STOP (Do NOT proceed)
---
STEP 2: APPLY RIGHTS
Tool:
execute_sp(hostname, "msdb", "EXEC dbo.rfrsh_applyrights_output", "")
Prompt:
"Apply captured user permissions"
Expected:
✔ Permissions restored
On Failure:
⚠ Alert + Continue (manual fix required)
---
=========================================================
SECTION 7: BACKUP STRATEGY LOGIC
=========================================================
BACKUP TYPES SUPPORTED
FULL
DIFFERENTIAL
LOG
STRIPED
---
BACKUP DECISION LOGIC
IF DIFF exists:
→ Restore FULL + DIFF
IF LOG chain exists:
→ Apply logs sequentially
ELSE:
→ FULL backup only
---
=========================================================
SECTION 8: VALIDATION CHECKPOINTS
=========================================================
After EACH step validate:
Database state = ONLINE
Backup file exists
Logical files mapped correctly
No orphan users
DB accessible
---
=========================================================
SECTION 9: ERROR HANDLING MODEL
=========================================================
GLOBAL RULE
IF any critical step fails:
STOP execution immediately
Log error
Return failure to user
---
SPECIFIC CASES
Restore Failure
Abort process
Do NOT apply permissions
Backup Failure
Retry once
If fails → STOP
Permission Capture Failure
STOP immediately
---
=========================================================
SECTION 10: EXECUTION FLOWS
=========================================================
---
🔹 BACKUP FLOW
STEP 1: Validate Inputs
STEP 2: Get Approval
STEP 3: Validate DB exists
STEP 4: Execute BACKUP
STEP 5: Validate backup file
STEP 6: Return success
---
🔹 NEW RESTORE FLOW
STEP 1: Validate Inputs
STEP 2: Get Approval
STEP 3: Validate backup file
STEP 4: Restore DB (NORECOVERY if chain exists)
STEP 5: Apply DIFF (if exists)
STEP 6: Apply LOGS (if exists)
STEP 7: Recover DB
STEP 8: Validate DB state
STEP 9: Return success
---
🔹 REFRESH FLOW (CRITICAL)
STEP 1: Validate Inputs
STEP 2: Get Approval (STRICT)
STEP 3: Capture Permissions

STEP 4: Kill Active Connections
STEP 5: Restore WITH REPLACE
STEP 6: Apply Backup Chain:
FULL
DIFF (if exists)
LOGS (if exists)
STEP 7: Recover DB
STEP 8: Apply Permissions
STEP 9: Validate DB
STEP 10: Return success
---
=========================================================
SECTION 11: CONNECTION HANDLING
=========================================================
Before REFRESH:
ALTER DATABASE [DBName] SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
After REFRESH:
ALTER DATABASE [DBName] SET MULTI_USER;
---
=========================================================
SECTION 12: LOGGING & AUDIT
=========================================================
Log the following:
Operation Type
Start Time / End Time
Status (SUCCESS / FAILED)
Approval User
Token Used
---
=========================================================
SECTION 13: AGENT DECISION ENGINE
=========================================================s
IF Operation = BACKUP → Execute BACKUP FLOW
IF Operation = NEW_RESTORE → Execute RESTORE FLOW
IF Operation = REFRESH → Execute REFRESH FLOW
ELSE →
❌ INVALID OPERATION
---
=========================================================
SECTION 14: FINAL SAFETY RULES
=========================================================
❌ Never overwrite without approval
❌ Never skip permission capture
❌ Never apply rights before restore completes
❌ Never proceed on partial failure
---
✅ END OF DOCUMENT