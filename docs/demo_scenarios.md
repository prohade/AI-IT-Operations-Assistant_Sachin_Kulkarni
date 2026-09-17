# Demo Scenarios

Use these during the assessment demonstration.

## 1. Knowledge search

**User:** `How do I reset my VPN password?`

Expected: agent calls Knowledge Search and returns local KB steps.

## 2. Ticket lookup

**User:** `Show me my VPN ticket status. My employee ID is EMP1024.`

Expected: agent calls Ticket Lookup and returns the matching SQLite ticket data.

## 3. Multi-turn memory

**User:** `My laptop camera is not working. Please create a ticket.`

Expected: assistant asks for missing employee ID.

**User:** `EMP1030`

Expected: the same conversation remembers the earlier camera issue and continues the workflow without requiring the problem to be repeated.

## 4. Duplicate prevention

**User:** `My VPN keeps disconnecting. Please create a ticket. My employee ID is EMP1024.`

Expected: agent checks existing active tickets and avoids creating a duplicate when an appropriate match already exists.

## 5. Missing information

**User:** `Create a ticket for me.`

Expected: assistant requests the required details instead of inventing them.

## 6. Nonexistent employee

**User:** `Create a laptop ticket for EMP9999 because the camera is not detected.`

Expected: employee validation fails gracefully and no ticket is created.
