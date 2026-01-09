# UI Preview - Dailyfix Messaging Platform

## Page 1: Login Page (`/`)

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│              Dailyfix Messaging                        │
│              Login to Matrix                           │
│                                                         │
│  ┌─────────────────────────────────────────────────┐  │
│  │ Username                                       │  │
│  │ [admin                                    ]    │  │
│  └─────────────────────────────────────────────────┘  │
│                                                         │
│  ┌─────────────────────────────────────────────────┐  │
│  │ Password                                       │  │
│  │ [••••••••••••••••••••••••••••••••••••••••]    │  │
│  └─────────────────────────────────────────────────┘  │
│                                                         │
│              [        Login        ]                    │
│                                                         │
│  ┌─────────────────────────────────────────────────┐  │
│  │ Default credentials:                            │  │
│  │ Username: admin                                 │  │
│  │ Password: admin123                              │  │
│  └─────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

**Features:**
- Clean, centered login form
- Username and password fields
- Default credentials displayed
- Error messages shown if login fails
- Auto-redirects if already logged in

---

## Page 2: Rooms List (`/rooms`)

```
┌─────────────────────────────────────────────────────────┐
│  Rooms                    @admin:localhost  [Logout]   │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────────┐  ┌──────────────────┐          │
│  │ General Chat     │  │ Support Room     │          │
│  │                  │  │                  │          │
│  │ #general:local...│  │ #support:local...│          │
│  └──────────────────┘  └──────────────────┘          │
│                                                         │
│  ┌──────────────────┐  ┌──────────────────┐          │
│  │ Instagram DM     │  │ Team Discussion  │          │
│  │                  │  │                  │          │
│  │ #instagram:local...│ #team:localhost...│          │
│  └──────────────────┘  └──────────────────┘          │
│                                                         │
│  ┌──────────────────┐                                 │
│  │ Customer Inquiry │                                 │
│  │                  │                                 │
│  │ #customer:local...│                                 │
│  └──────────────────┘                                 │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**Features:**
- Header with user ID and logout button
- Grid layout of room cards
- Room name, topic, and ID displayed
- Clickable cards that navigate to chat
- Auto-refreshes every 5 seconds
- Empty state if no rooms

---

## Page 3: Chat View (`/chat?roomId=...`)

```
┌─────────────────────────────────────────────────────────┐
│  ← Back to Rooms    General Chat        [Show AI Features]│
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────────────────────────────────────────┐  │
│  │ AI Features                                     │  │
│  │                                                  │  │
│  │  [Summarize Conversation]                        │  │
│  │  [Prioritize Messages]                          │  │
│  │  [Generate Daily Report]                        │  │
│  │                                                  │  │
│  │  Summary:                                        │  │
│  │  Customer inquired about order status...         │  │
│  └─────────────────────────────────────────────────┘  │
│                                                         │
│  ┌─────────────────────────────────────────────────┐  │
│  │ @user1:localhost                                │  │
│  │ 2024-01-15 10:30 AM                             │  │
│  │ Hello, I need help with my order               │  │
│  └─────────────────────────────────────────────────┘  │
│                                                         │
│  ┌─────────────────────────────────────────────────┐  │
│  │ @admin:localhost                                │  │
│  │ 2024-01-15 10:31 AM                             │  │
│  │ Sure, how can I assist you?                     │  │
│  └─────────────────────────────────────────────────┘  │
│                                                         │
│  ┌─────────────────────────────────────────────────┐  │
│  │ @user1:localhost                                │  │
│  │ 2024-01-15 10:32 AM                             │  │
│  │ My order #12345 is delayed. This is urgent!     │  │
│  └─────────────────────────────────────────────────┘  │
│                                                         │
│  ┌─────────────────────────────────────────────────┐  │
│  │ @admin:localhost                                │  │
│  │ 2024-01-15 10:33 AM                             │  │
│  │ I'll check on that right away for you.          │  │
│  └─────────────────────────────────────────────────┘  │
│                                                         │
├─────────────────────────────────────────────────────────┤
│  [Type a message...                    ]  [Send]      │
└─────────────────────────────────────────────────────────┘
```

**Features:**
- Back button to return to rooms
- Room name in header
- Toggle AI features panel
- Message list with:
  - User ID and timestamp
  - Message body
  - Styled message bubbles
- Message input at bottom
- Send button
- Auto-refreshes every 3 seconds
- AI features panel with:
  - Summarize button
  - Prioritize button
  - Daily report button
  - Results display area

---

## AI Features Panel (Expanded)

```
┌─────────────────────────────────────────────────────────┐
│  AI Features                                    [Hide]   │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  [Summarize Conversation]  [Prioritize]  [Daily Report] │
│                                                         │
│  ┌─────────────────────────────────────────────────┐  │
│  │ Summary:                                         │  │
│  │ Customer inquired about delayed order. Admin    │  │
│  │ provided assistance and checked order status.    │  │
│  │ Issue resolved satisfactorily.                  │  │
│  └─────────────────────────────────────────────────┘  │
│                                                         │
│  ┌─────────────────────────────────────────────────┐  │
│  │ Top Priority Messages:                          │  │
│  │ • Score: 8.5 - URGENT: System is down!          │  │
│  │ • Score: 6.2 - My order is delayed...          │  │
│  │ • Score: 3.1 - I have a question about...       │  │
│  └─────────────────────────────────────────────────┘  │
│                                                         │
│  ┌─────────────────────────────────────────────────┐  │
│  │ Daily Report:                                    │  │
│  │ Total Messages: 15                               │  │
│  │ Summary: Handled customer inquiries...          │  │
│  │                                                  │  │
│  │ Key Insights:                                    │  │
│  │ • 2 complaint(s) require follow-up              │  │
│  │ • Multiple questions detected                   │  │
│  └─────────────────────────────────────────────────┘  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## Color Scheme & Styling

**Colors:**
- Primary Blue: `#007bff` (buttons, links)
- Success Green: `#28a745` (AI features)
- Danger Red: `#dc3545` (logout, errors)
- Background: `#f5f5f5` (light gray)
- Cards: `#ffffff` (white)
- Text: `#333333` (dark gray)
- Secondary Text: `#666666` (medium gray)
- Borders: `#dddddd` (light gray)

**Typography:**
- Headers: Bold, 20-28px
- Body: 14-16px, regular weight
- Code/IDs: Monospace, 12px

**Layout:**
- Max width: 1200px (centered)
- Padding: 20px
- Border radius: 8px (cards), 4px (buttons)
- Box shadow: Subtle elevation on cards

---

## Responsive Design

**Desktop (>768px):**
- Multi-column grid for rooms
- Full-width chat view
- Side-by-side AI panel

**Mobile (<768px):**
- Single column layout
- Stacked room cards
- Full-width chat messages
- Collapsible AI panel

---

## User Flow

```
Login Page
    ↓ (Enter credentials)
Rooms List
    ↓ (Click room)
Chat View
    ↓ (Toggle AI Features)
AI Analysis Results
    ↓ (Send message)
Updated Chat View
```

---

## Interactive Elements

1. **Login Form**
   - Username input (text)
   - Password input (password)
   - Login button (submit)
   - Error message display

2. **Room Cards**
   - Hover effect (slight elevation)
   - Click to navigate
   - Room name, topic, ID

3. **Chat Interface**
   - Message bubbles
   - Timestamp display
   - User ID badges
   - Input field
   - Send button
   - Auto-scroll to latest

4. **AI Features**
   - Toggle button
   - Action buttons
   - Loading states
   - Results display
   - Collapsible sections

---

## Screenshots Description

**Login Page:**
- Centered white card on gray background
- Clean form with two inputs
- Blue login button
- Info box with default credentials

**Rooms Page:**
- Header bar with title and user info
- Grid of white cards
- Each card shows room name and ID
- Logout button in header

**Chat Page:**
- Full-height layout
- Header with navigation
- Scrollable message area
- Fixed input at bottom
- Expandable AI panel at top

---

**Note:** This is a functional MVP UI focused on usability rather than design polish. The interface is clean, responsive, and fully functional for demo purposes.
