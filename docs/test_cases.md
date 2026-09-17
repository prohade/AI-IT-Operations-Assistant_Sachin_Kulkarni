# Test Cases

| ID | Scenario | Expected Result |
|---|---|---|
| TC01 | VPN password question | Knowledge Search tool is selected and KB answer returned |
| TC02 | Ticket status with EMP1024 | Ticket Lookup returns database record(s) |
| TC03 | Ticket ID lookup | Requested ticket details are returned without invented fields |
| TC04 | Ticket creation without employee ID | Assistant asks for missing employee ID |
| TC05 | Follow-up employee ID only | Conversation state retains the earlier issue |
| TC06 | Duplicate VPN ticket for EMP1024 | Duplicate is detected and unnecessary creation is prevented |
| TC07 | Invalid employee | Ticket creation is blocked |
| TC08 | Empty required ticket information | Tool returns validation error |
| TC09 | Unknown KB issue | Assistant reports no matching local article or gives clearly generated guidance |
| TC10 | API failure | UI shows a friendly error and technical detail only in an expander |
| TC11 | Clear / Reset | New conversation thread starts and prior chat is cleared |
| TC12 | Tool visibility | Tool/action details are visible below the assistant response |
