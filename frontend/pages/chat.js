import { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import Link from 'next/link';
import { matrixClient, aiClient } from '../services/matrix';

export default function Chat() {
  const router = useRouter();
  const { roomId } = router.query;
  
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [loading, setLoading] = useState(true);
  const [sending, setSending] = useState(false);
  const [error, setError] = useState('');
  const [roomName, setRoomName] = useState('');
  
  // AI Features
  const [showAIFeatures, setShowAIFeatures] = useState(false);
  const [summary, setSummary] = useState('');
  const [prioritized, setPrioritized] = useState([]);
  const [dailyReport, setDailyReport] = useState(null);
  const [aiLoading, setAiLoading] = useState(false);

  useEffect(() => {
    if (!roomId) return;
    
    // Check authentication
    if (!matrixClient.restoreSession()) {
      router.push('/');
      return;
    }

    loadRoomInfo();
    loadMessages();
    
    // Poll for new messages every 3 seconds
    const interval = setInterval(loadMessages, 3000);
    return () => clearInterval(interval);
  }, [roomId, router]);

  const loadRoomInfo = async () => {
    try {
      const state = await matrixClient.getRoomDetails(roomId);
      const nameEvent = state.find(e => e.type === 'm.room.name');
      setRoomName(nameEvent?.content?.name || roomId);
    } catch (err) {
      console.error('Error loading room info:', err);
    }
  };

  const loadMessages = async () => {
    try {
      const data = await matrixClient.getMessages(roomId, 50);
      const formattedMessages = (data.messages || []).map(msg => ({
        id: msg.event_id,
        body: msg.content?.body || '',
        user_id: msg.sender,
        timestamp: msg.origin_server_ts,
        type: msg.content?.msgtype || 'm.text',
      })).reverse(); // Reverse to show oldest first
      
      setMessages(formattedMessages);
      setError('');
    } catch (err) {
      setError(err.message || 'Failed to load messages');
      console.error('Error loading messages:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!newMessage.trim() || sending) return;

    setSending(true);
    try {
      await matrixClient.sendMessage(roomId, newMessage);
      setNewMessage('');
      // Reload messages after a short delay
      setTimeout(loadMessages, 500);
    } catch (err) {
      setError(err.message || 'Failed to send message');
    } finally {
      setSending(false);
    }
  };

  const handleSummarize = async () => {
    if (messages.length === 0) return;
    
    setAiLoading(true);
    try {
      const conversationText = messages
        .map(m => `${m.user_id}: ${m.body}`)
        .join('\n');
      
      const result = await aiClient.summarize(conversationText);
      setSummary(result.summary);
    } catch (err) {
      setError('Failed to generate summary');
    } finally {
      setAiLoading(false);
    }
  };

  const handlePrioritize = async () => {
    if (messages.length === 0) return;
    
    setAiLoading(true);
    try {
      const result = await aiClient.prioritize(messages);
      setPrioritized(result.ranked_messages);
    } catch (err) {
      setError('Failed to prioritize messages');
    } finally {
      setAiLoading(false);
    }
  };

  const handleDailyReport = async () => {
    if (messages.length === 0) return;
    
    setAiLoading(true);
    try {
      const today = new Date().toISOString().split('T')[0];
      const result = await aiClient.generateDailyReport(
        matrixClient.userId,
        today,
        [{
          id: roomId,
          messages: messages,
        }]
      );
      setDailyReport(result);
    } catch (err) {
      setError('Failed to generate daily report');
    } finally {
      setAiLoading(false);
    }
  };

  const formatTimestamp = (timestamp) => {
    if (!timestamp) return '';
    const date = new Date(timestamp);
    return date.toLocaleString();
  };

  if (loading) {
    return (
      <div style={styles.container}>
        <div style={styles.loading}>Loading messages...</div>
      </div>
    );
  }

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <Link href="/rooms" style={styles.backLink}>← Back to Rooms</Link>
        <h2 style={styles.roomTitle}>{roomName}</h2>
        <button
          onClick={() => setShowAIFeatures(!showAIFeatures)}
          style={styles.aiButton}
        >
          {showAIFeatures ? 'Hide' : 'Show'} AI Features
        </button>
      </div>

      {error && <div style={styles.error}>{error}</div>}

      {showAIFeatures && (
        <div style={styles.aiPanel}>
          <h3>AI Features</h3>
          <div style={styles.aiButtons}>
            <button
              onClick={handleSummarize}
              disabled={aiLoading || messages.length === 0}
              style={styles.aiFeatureButton}
            >
              Summarize Conversation
            </button>
            <button
              onClick={handlePrioritize}
              disabled={aiLoading || messages.length === 0}
              style={styles.aiFeatureButton}
            >
              Prioritize Messages
            </button>
            <button
              onClick={handleDailyReport}
              disabled={aiLoading || messages.length === 0}
              style={styles.aiFeatureButton}
            >
              Generate Daily Report
            </button>
          </div>

          {aiLoading && <div style={styles.loading}>Processing...</div>}

          {summary && (
            <div style={styles.aiResult}>
              <h4>Summary:</h4>
              <p>{summary}</p>
            </div>
          )}

          {prioritized.length > 0 && (
            <div style={styles.aiResult}>
              <h4>Top Priority Messages:</h4>
              <ul>
                {prioritized.slice(0, 5).map((msg, idx) => (
                  <li key={idx} style={styles.priorityItem}>
                    <strong>Score: {msg.priority_score}</strong> - {msg.body}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {dailyReport && (
            <div style={styles.aiResult}>
              <h4>Daily Report:</h4>
              <p><strong>Total Messages:</strong> {dailyReport.total_messages}</p>
              <p><strong>Summary:</strong> {dailyReport.summary}</p>
              <p><strong>Key Insights:</strong></p>
              <ul>
                {dailyReport.key_insights.map((insight, idx) => (
                  <li key={idx}>{insight}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}

      <div style={styles.messagesContainer}>
        {messages.length === 0 ? (
          <div style={styles.empty}>No messages yet. Start the conversation!</div>
        ) : (
          messages.map((msg) => (
            <div key={msg.id} style={styles.message}>
              <div style={styles.messageHeader}>
                <strong style={styles.messageUser}>{msg.user_id}</strong>
                <span style={styles.messageTime}>{formatTimestamp(msg.timestamp)}</span>
              </div>
              <div style={styles.messageBody}>{msg.body}</div>
            </div>
          ))
        )}
      </div>

      <form onSubmit={handleSendMessage} style={styles.inputForm}>
        <input
          type="text"
          value={newMessage}
          onChange={(e) => setNewMessage(e.target.value)}
          placeholder="Type a message..."
          style={styles.input}
          disabled={sending}
        />
        <button
          type="submit"
          disabled={sending || !newMessage.trim()}
          style={styles.sendButton}
        >
          {sending ? 'Sending...' : 'Send'}
        </button>
      </form>
    </div>
  );
}

const styles = {
  container: {
    display: 'flex',
    flexDirection: 'column',
    height: '100vh',
    backgroundColor: '#f5f5f5',
  },
  header: {
    backgroundColor: 'white',
    padding: '15px 20px',
    borderBottom: '1px solid #ddd',
    display: 'flex',
    alignItems: 'center',
    gap: '15px',
  },
  backLink: {
    color: '#007bff',
    textDecoration: 'none',
    fontSize: '14px',
  },
  roomTitle: {
    flex: 1,
    margin: 0,
    fontSize: '20px',
    color: '#333',
  },
  aiButton: {
    padding: '8px 16px',
    backgroundColor: '#28a745',
    color: 'white',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
    fontSize: '14px',
  },
  aiPanel: {
    backgroundColor: 'white',
    padding: '20px',
    borderBottom: '1px solid #ddd',
  },
  aiButtons: {
    display: 'flex',
    gap: '10px',
    marginBottom: '15px',
    flexWrap: 'wrap',
  },
  aiFeatureButton: {
    padding: '8px 16px',
    backgroundColor: '#007bff',
    color: 'white',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
    fontSize: '14px',
  },
  aiResult: {
    marginTop: '15px',
    padding: '15px',
    backgroundColor: '#f8f9fa',
    borderRadius: '4px',
  },
  priorityItem: {
    marginBottom: '8px',
  },
  messagesContainer: {
    flex: 1,
    overflowY: 'auto',
    padding: '20px',
  },
  message: {
    backgroundColor: 'white',
    padding: '15px',
    marginBottom: '10px',
    borderRadius: '8px',
    boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
  },
  messageHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    marginBottom: '8px',
  },
  messageUser: {
    color: '#333',
    fontSize: '14px',
  },
  messageTime: {
    color: '#999',
    fontSize: '12px',
  },
  messageBody: {
    color: '#555',
    fontSize: '15px',
    lineHeight: '1.5',
  },
  empty: {
    textAlign: 'center',
    padding: '40px',
    color: '#666',
  },
  inputForm: {
    display: 'flex',
    padding: '15px 20px',
    backgroundColor: 'white',
    borderTop: '1px solid #ddd',
    gap: '10px',
  },
  input: {
    flex: 1,
    padding: '12px',
    border: '1px solid #ddd',
    borderRadius: '4px',
    fontSize: '16px',
  },
  sendButton: {
    padding: '12px 24px',
    backgroundColor: '#007bff',
    color: 'white',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
    fontSize: '16px',
  },
  error: {
    backgroundColor: '#fee',
    color: '#c33',
    padding: '12px',
    margin: '10px 20px',
    borderRadius: '4px',
  },
  loading: {
    textAlign: 'center',
    padding: '20px',
    color: '#666',
  },
};
