/**
 * Matrix Client Service
 * Handles all Matrix API interactions
 */

const MATRIX_SERVER = process.env.NEXT_PUBLIC_MATRIX_SERVER || 'http://localhost:8008';
const AI_BACKEND = process.env.NEXT_PUBLIC_AI_BACKEND || 'http://localhost:8000';

class MatrixClient {
  constructor() {
    this.baseUrl = MATRIX_SERVER;
    this.accessToken = null;
    this.userId = null;
  }

  /**
   * Login to Matrix server
   */
  async login(username, password) {
    try {
      const response = await fetch(`${this.baseUrl}/_matrix/client/r0/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          type: 'm.login.password',
          user: username,
          password: password,
        }),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || 'Login failed');
      }

      const data = await response.json();
      this.accessToken = data.access_token;
      this.userId = data.user_id;
      
      // Store in localStorage
      if (typeof window !== 'undefined') {
        localStorage.setItem('matrix_access_token', this.accessToken);
        localStorage.setItem('matrix_user_id', this.userId);
      }

      return data;
    } catch (error) {
      console.error('Login error:', error);
      throw error;
    }
  }

  /**
   * Restore session from localStorage
   */
  restoreSession() {
    if (typeof window !== 'undefined') {
      this.accessToken = localStorage.getItem('matrix_access_token');
      this.userId = localStorage.getItem('matrix_user_id');
    }
    return this.accessToken !== null;
  }

  /**
   * Logout
   */
  logout() {
    this.accessToken = null;
    this.userId = null;
    if (typeof window !== 'undefined') {
      localStorage.removeItem('matrix_access_token');
      localStorage.removeItem('matrix_user_id');
    }
  }

  /**
   * Get authenticated headers
   */
  getHeaders() {
    const headers = {
      'Content-Type': 'application/json',
    };
    if (this.accessToken) {
      headers['Authorization'] = `Bearer ${this.accessToken}`;
    }
    return headers;
  }

  /**
   * Get joined rooms
   */
  async getJoinedRooms() {
    if (!this.accessToken) {
      throw new Error('Not authenticated');
    }

    try {
      const response = await fetch(
        `${this.baseUrl}/_matrix/client/r0/joined_rooms`,
        {
          headers: this.getHeaders(),
        }
      );

      if (!response.ok) {
        throw new Error('Failed to fetch rooms');
      }

      const data = await response.json();
      return data.joined_rooms || [];
    } catch (error) {
      console.error('Error fetching rooms:', error);
      throw error;
    }
  }

  /**
   * Get room details
   */
  async getRoomDetails(roomId) {
    if (!this.accessToken) {
      throw new Error('Not authenticated');
    }

    try {
      const response = await fetch(
        `${this.baseUrl}/_matrix/client/r0/rooms/${roomId}/state`,
        {
          headers: this.getHeaders(),
        }
      );

      if (!response.ok) {
        throw new Error('Failed to fetch room details');
      }

      return await response.json();
    } catch (error) {
      console.error('Error fetching room details:', error);
      throw error;
    }
  }

  /**
   * Get messages from a room
   */
  async getMessages(roomId, limit = 50, from = null) {
    if (!this.accessToken) {
      throw new Error('Not authenticated');
    }

    try {
      let url = `${this.baseUrl}/_matrix/client/r0/rooms/${roomId}/messages?limit=${limit}`;
      if (from) {
        url += `&from=${from}`;
      }

      const response = await fetch(url, {
        headers: this.getHeaders(),
      });

      if (!response.ok) {
        throw new Error('Failed to fetch messages');
      }

      const data = await response.json();
      return {
        messages: data.chunk || [],
        next_batch: data.end || null,
      };
    } catch (error) {
      console.error('Error fetching messages:', error);
      throw error;
    }
  }

  /**
   * Send a message to a room
   */
  async sendMessage(roomId, message) {
    if (!this.accessToken) {
      throw new Error('Not authenticated');
    }

    try {
      const txnId = Date.now().toString();
      const response = await fetch(
        `${this.baseUrl}/_matrix/client/r0/rooms/${roomId}/send/m.room.message/${txnId}`,
        {
          method: 'PUT',
          headers: this.getHeaders(),
          body: JSON.stringify({
            msgtype: 'm.text',
            body: message,
          }),
        }
      );

      if (!response.ok) {
        throw new Error('Failed to send message');
      }

      return await response.json();
    } catch (error) {
      console.error('Error sending message:', error);
      throw error;
    }
  }
}

// AI Backend Service
class AIClient {
  constructor() {
    this.baseUrl = AI_BACKEND;
  }

  async summarize(text) {
    try {
      const response = await fetch(`${this.baseUrl}/summarize`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text }),
      });

      if (!response.ok) {
        throw new Error('Summarization failed');
      }

      return await response.json();
    } catch (error) {
      console.error('Error summarizing:', error);
      throw error;
    }
  }

  async parseIntent(message) {
    try {
      const response = await fetch(`${this.baseUrl}/intent`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message }),
      });

      if (!response.ok) {
        throw new Error('Intent parsing failed');
      }

      return await response.json();
    } catch (error) {
      console.error('Error parsing intent:', error);
      throw error;
    }
  }

  async prioritize(messages) {
    try {
      const response = await fetch(`${this.baseUrl}/priority`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ messages }),
      });

      if (!response.ok) {
        throw new Error('Prioritization failed');
      }

      return await response.json();
    } catch (error) {
      console.error('Error prioritizing:', error);
      throw error;
    }
  }

  async generateDailyReport(userId, date, conversations) {
    try {
      const response = await fetch(`${this.baseUrl}/daily-report`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_id: userId,
          date: date,
          conversations: conversations,
        }),
      });

      if (!response.ok) {
        throw new Error('Report generation failed');
      }

      return await response.json();
    } catch (error) {
      console.error('Error generating report:', error);
      throw error;
    }
  }

  async vectorSearch(query) {
    try {
      const response = await fetch(`${this.baseUrl}/vector/search`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query, top_k: 5 }),
      });

      if (!response.ok) {
        throw new Error('Vector search failed');
      }

      return await response.json();
    } catch (error) {
      console.error('Error in vector search:', error);
      throw error;
    }
  }
}

// Export singleton instances
export const matrixClient = new MatrixClient();
export const aiClient = new AIClient();
