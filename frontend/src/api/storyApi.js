const API_BASE_URL = 'https://story-frontend-zuu1.vercel.app';

export const storyApi = {
    generateStory: async (prefix, maxLength = 200) => {
        try {
            const response = await fetch(`${API_BASE_URL}/generate`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ prefix, max_length: maxLength })
            });

            if (!response.ok) throw new Error('Failed to generate story');

            const data = await response.json();
            return data.generated_text;
        } catch (error) {
            console.error('Story API Error:', error);
            throw error;
        }
    },

    generateStoryStream: async (prefix, onToken, maxLength = 200) => {
        try {
            const response = await fetch(`${API_BASE_URL}/generate-stream`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ prefix, max_length: maxLength })
            });

            if (!response.ok) throw new Error('Failed to start stream');

            const reader = response.body.getReader();
            const decoder = new TextDecoder();

            while (true) {
                const { done, value } = await reader.read();
                if (done) break;
                const chunk = decoder.decode(value, { stream: true });
                onToken(chunk);
            }
        } catch (error) {
            console.error('Streaming Error:', error);
            throw error;
        }
    }
};
