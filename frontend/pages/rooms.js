import { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import Link from 'next/link';
import { matrixClient } from '../services/matrix';

export default function Rooms() {
  const router = useRouter();
  const [rooms, setRooms] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [userId, setUserId] = useState('');

  useEffect(() => {
    // Check authentication
    if (!matrixClient.restoreSession()) {
      router.push('/');
      return;
    }

    setUserId(matrixClient.userId);
    loadRooms();
    
    // Poll for updates every 5 seconds
    const interval = setInterval(loadRooms, 5000);
    return () => clearInterval(interval);
  }, [router]);

  const loadRooms = async () => {
    try {
      const roomIds = await matrixClient.getJoinedRooms();
      
      // Fetch details for each room
      const roomDetails = await Promise.all(
        roomIds.map(async (roomId) => {
          try {
            const state = await matrixClient.getRoomDetails(roomId);
            const nameEvent = state.find(e => e.type === 'm.room.name');
            const topicEvent = state.find(e => e.type === 'm.room.topic');
            
            return {
              id: roomId,
              name: nameEvent?.content?.name || roomId,
              topic: topicEvent?.content?.topic || '',
            };
          } catch (err) {
            return {
              id: roomId,
              name: roomId,
              topic: '',
            };
          }
        })
      );
      
      setRooms(roomDetails);
      setError('');
    } catch (err) {
      setError(err.message || 'Failed to load rooms');
      console.error('Error loading rooms:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    matrixClient.logout();
    router.push('/');
  };

  if (loading) {
    return (
      <div style={styles.container}>
        <div style={styles.loading}>Loading rooms...</div>
      </div>
    );
  }

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <h1 style={styles.title}>Rooms</h1>
        <div style={styles.userInfo}>
          <span style={styles.userId}>{userId}</span>
          <button onClick={handleLogout} style={styles.logoutButton}>
            Logout
          </button>
        </div>
      </div>

      {error && <div style={styles.error}>{error}</div>}

      <div style={styles.roomsList}>
        {rooms.length === 0 ? (
          <div style={styles.empty}>
            <p>No rooms found. Create a room or wait for messages.</p>
          </div>
        ) : (
          rooms.map((room) => (
            <Link key={room.id} href={`/chat?roomId=${room.id}`}>
              <div style={styles.roomCard}>
                <h3 style={styles.roomName}>{room.name}</h3>
                {room.topic && <p style={styles.roomTopic}>{room.topic}</p>}
                <p style={styles.roomId}>{room.id}</p>
              </div>
            </Link>
          ))
        )}
      </div>
    </div>
  );
}

const styles = {
  container: {
    minHeight: '100vh',
    backgroundColor: '#f5f5f5',
    padding: '20px',
  },
  header: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '30px',
    backgroundColor: 'white',
    padding: '20px',
    borderRadius: '8px',
    boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
  },
  title: {
    fontSize: '28px',
    fontWeight: 'bold',
    color: '#333',
    margin: 0,
  },
  userInfo: {
    display: 'flex',
    alignItems: 'center',
    gap: '15px',
  },
  userId: {
    fontSize: '14px',
    color: '#666',
  },
  logoutButton: {
    padding: '8px 16px',
    backgroundColor: '#dc3545',
    color: 'white',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
    fontSize: '14px',
  },
  error: {
    backgroundColor: '#fee',
    color: '#c33',
    padding: '12px',
    borderRadius: '4px',
    marginBottom: '20px',
  },
  roomsList: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))',
    gap: '20px',
  },
  roomCard: {
    backgroundColor: 'white',
    padding: '20px',
    borderRadius: '8px',
    boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
    cursor: 'pointer',
    transition: 'transform 0.2s, box-shadow 0.2s',
  },
  roomCardHover: {
    transform: 'translateY(-2px)',
    boxShadow: '0 4px 8px rgba(0,0,0,0.15)',
  },
  roomName: {
    fontSize: '18px',
    fontWeight: '600',
    color: '#333',
    marginBottom: '8px',
  },
  roomTopic: {
    fontSize: '14px',
    color: '#666',
    marginBottom: '8px',
  },
  roomId: {
    fontSize: '12px',
    color: '#999',
    fontFamily: 'monospace',
    wordBreak: 'break-all',
  },
  empty: {
    textAlign: 'center',
    padding: '40px',
    color: '#666',
  },
  loading: {
    textAlign: 'center',
    padding: '40px',
    fontSize: '18px',
    color: '#666',
  },
};
