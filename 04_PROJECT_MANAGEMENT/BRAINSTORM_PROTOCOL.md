# 🧠 Brainstorm Protocol

**Version**: 1.0  
**Status**: ACTIVE  
**Last Updated**: November 23, 2025

---

## 🎯 **1. Purpose**

This protocol establishes a **persistent, non-executing brainstorming mode** designed for dynamic, free-flowing ideation and strategic discussion. When this protocol is active, the agent will not take any executive actions (e.g., file edits, shell commands, code execution) and will engage purely in conversation to explore ideas, concepts, and strategies.

This allows for a safe and creative space to think without committing to any changes or actions.

---

## ⚙️ **2. Rules of Engagement**

### **Activation**
- **Command**: The user must explicitly state `Activate Brainstorm Protocol`, `Begin Brainstorm`, or a similar clear intent.
- **Confirmation**: The agent will confirm activation with a message, indicating that Brainstorm Mode is now active.

### **Deactivation**
- **Command**: The user must explicitly state `End Brainstorm Protocol`, `Conclude Brainstorm`, or a similar clear intent.
- **Confirmation**: The agent will confirm deactivation and return to standard operational mode.

### **Agent Behavior in Brainstorm Mode**

1.  **No Tool Use**: The agent **WILL NOT** use any tools to execute actions. All file operations, shell commands, code execution, and other executive functions are suspended.
2.  **Message-Only Interaction**: The agent will ONLY use the `message` tool (with `type: 'info'` or `type: 'ask'`) to communicate. This ensures a purely conversational flow.
3.  **Persistence**: The mode is **persistent** across multiple user prompts. It remains active until the user explicitly deactivates it. There is no need to invoke the protocol in every prompt.
4.  **Ephemeral Ideas**: All ideas, suggestions, and discussions within the brainstorm session are considered **ephemeral** and will not be automatically logged, saved, or committed to the project. This encourages free thinking without consequence.
5.  **Post-Session Action**: After the session is concluded, the user can then instruct the agent to implement any of the ideas discussed. The agent will then proceed with its standard execution workflow.

---

## 🏛️ **3. Governance**

- This protocol is a sub-protocol of the main **[Protocol Governance System](00_DATABASE/PROTOCOL_GOVERNANCE_SYSTEM.md)**.
- It can be activated at any time, regardless of the current project phase or active persona (Vedic Sage or Systems Architect).
- The agent is responsible for strictly adhering to the non-execution rule while the protocol is active.

---

## 🚀 **4. Example Usage**

**User**: `Activate Brainstorm Protocol`

**Agent**: `🧠 **Brainstorm Mode Activated!** I will not execute any actions. Let's ideate freely. What's on your mind?`

**(Dynamic back-and-forth discussion ensues...)**

**User**: `Great, I think we have a solid plan. Conclude Brainstorm.`

**Agent**: `✅ **Brainstorm Mode Deactivated.** Returning to standard operational mode. I am ready to execute the plan we discussed. Please provide your instructions.`

---
