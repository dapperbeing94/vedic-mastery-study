> **Vedic Mastery Study v2.0 - Repository Cleanup Protocol v2.0**
> **Last Updated**: November 23, 2025
> **Status**: ACTIVE

---

## 1. PURPOSE

This protocol provides a safe, systematic, and reversible process for cleaning up the repository by archiving obsolete files and restructuring directories. Its primary goal is to maintain a clean, logical, and efficient repository structure without risking the loss of vital data or institutional knowledge.

**The core principle is: Archive, Never Delete.**

---

## 2. SCOPE

This protocol applies to:
-   Obsolete study documents.
-   Temporary research files.
-   Redundant or outdated scripts.
-   Empty or illogical directories.
-   Any file or directory that is no longer relevant to the project's v2 architecture.

---

## 3. CLEANUP CATEGORIES & RISK LEVELS

Before any action is taken, every file/directory targeted for cleanup must be assigned a category and risk level.

| Category | Description | Risk Level | Action |
| :--- | :--- | :--- | :--- |
| **A: Obsolete Documents** | Old study notes, temporary research files, previous versions of protocols. | **Low** | Move to `04_ARCHIVES/documents/` |
| **B: Redundant Scripts** | Old versions of tracking scripts, one-off analysis scripts. | **Medium** | Move to `04_ARCHIVES/scripts/` |
| **C: Structural Duplicates** | Duplicate directory structures (e.g., old numbered category folders). | **Medium** | Consolidate content, then move empty directories to `04_ARCHIVES/structure/` |
| **D: Critical System Files** | Anything in `00_DATABASE/`, core protocols, the master plan. | **High** | **DO NOT TOUCH**. These are not eligible for cleanup under this protocol. |

---

## 4. CLEANUP WORKFLOW

This workflow is executed by the `cleanup_analyzer.py` script and overseen by the Systems Architect persona.

### 4.1. Step 1: Analysis & Proposal Generation

1.  **Scan Repository**: The `cleanup_analyzer.py` script scans the entire repository.
2.  **Identify Candidates**: It identifies files/directories that are candidates for cleanup based on a set of rules (e.g., not linked in the database, older than a certain date, located in a deprecated path).
3.  **Generate Proposal**: It generates a `cleanup_proposal.json` file, which lists every candidate file, its assigned category (A, B, or C), and the proposed action (e.g., "Move to `04_ARCHIVES/documents/`").

### 4.2. Step 2: User Review & Approval (Critical Gate)

1.  **Present Proposal**: The contents of `cleanup_proposal.json` are presented to the user in a readable format.
2.  **User Decision**: The user reviews the list and can approve, reject, or re-categorize any item.
3.  **Finalize Plan**: The `cleanup_proposal.json` is updated with the user's final decisions.

### 4.3. Step 3: Backup & Execution

1.  **Create Pre-Cleanup Backup**: A full, timestamped backup of the repository is created immediately before execution.
2.  **Execute Plan**: A script iterates through the approved `cleanup_proposal.json` and executes the `mv` commands to move the files to the appropriate archive directory.
3.  **Log Actions**: Every `mv` operation is logged to a `cleanup_log.txt` file, creating an audit trail.

### 4.4. Step 4: Validation

1.  **Verify Moves**: The script verifies that all targeted files are now in the archive and no longer in their original locations.
2.  **Run System Health Check**: Key scripts are run (e.g., `depth_tracker.py`) to ensure that the cleanup has not broken any critical functionality.
3.  **Check for Broken Links**: The system scans for any internal links that may have been broken by the move.

### 4.5. Step 5: Commit

-   Once validation is successful, the changes (file moves and the new log file) are committed to GitHub with a clear message (e.g., "Execute repository cleanup based on proposal YYYY-MM-DD").

---

## 5. ROLLBACK PROCEDURE

If the cleanup process causes any critical failures, the rollback procedure is simple and safe.

1.  **Identify Pre-Cleanup Backup**: Locate the backup created in Step 4.3.
2.  **Delete Corrupted Repository**: `rm -rf /home/ubuntu/vedic-mastery-study`
3.  **Restore from Backup**: `cp -r /path/to/backup/vedic-mastery-study /home/ubuntu/`
4.  **Validate**: Confirm the repository is restored to its pre-cleanup state.

---

## 6. THE `04_ARCHIVES` DIRECTORY

The archive directory is a permanent, read-only part of the repository. It is structured to mirror the project's main directories.

```
04_ARCHIVES/
├── documents/      # Old study notes, research files
├── scripts/        # Deprecated scripts
├── structure/      # Empty, obsolete directory structures
└── logs/           # Logs of all cleanup operations
```

This ensures that we never truly delete anything, preserving the project's history while keeping the main working directories clean and efficient.
