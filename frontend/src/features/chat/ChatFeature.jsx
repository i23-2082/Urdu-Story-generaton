import React, { useState, useRef, useEffect } from 'react';
import { storyApi } from '../../api/storyApi';

const ChatFeature = ({ messages, setMessages, isLoading, setIsLoading }) => {
    const [input, setInput] = useState('');
    const chatContainerRef = useRef(null);

    useEffect(() => {
        if (chatContainerRef.current) {
            chatContainerRef.current.scrollTo({
                top: chatContainerRef.current.scrollHeight,
                behavior: 'smooth'
            });
        }
    }, [messages, isLoading]);

    const handleSend = async () => {
        if (!input.trim() || isLoading) return;

        const userMessage = { role: 'user', content: input, isUrdu: true };
        setMessages(prev => [...prev, userMessage]);
        setInput('');
        setIsLoading(true);

        // Initial AI message placeholder
        const aiMessage = { role: 'ai', content: '', isUrdu: true };
        setMessages(prev => [...prev, aiMessage]);

        try {
            let fullText = input + ' ';
            await storyApi.generateStoryStream(input, (token) => {
                fullText += token;
                setMessages(prev => {
                    const newMessages = [...prev];
                    const lastMsgIndex = newMessages.length - 1;
                    if (lastMsgIndex >= 0) {
                        newMessages[lastMsgIndex] = { ...newMessages[lastMsgIndex], content: fullText };
                    }
                    return newMessages;
                });
            });
        } catch (error) {
            setMessages(prev => {
                const newMessages = [...prev];
                const lastMsgIndex = newMessages.length - 1;
                if (lastMsgIndex >= 0) {
                    newMessages[lastMsgIndex] = {
                        ...newMessages[lastMsgIndex],
                        content: 'معذرت، کہانی تیار کرتے وقت کچھ غلطی ہو گئی۔ براہ کرم دوبارہ کوشش کریں۔'
                    };
                }
                return newMessages;
            });
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="flex-1 flex flex-col h-full bg-chat-bg overflow-hidden">
            {/* Messages */}
            <div className="flex-1 overflow-y-auto scroll-smooth py-10 px-4 md:px-0" ref={chatContainerRef}>
                <div className="max-w-3xl mx-auto flex flex-col">
                    {messages.map((msg, i) => (
                        <div
                            key={i}
                            className={`flex gap-5 mb-10 w-full group ${msg.role === 'user' ? 'flex-row-reverse' : ''}`}
                        >
                            <div className={`w-10 h-10 rounded-full flex items-center justify-center shrink-0 border mt-1 shadow-sm ${msg.role === 'ai'
                                ? 'bg-accent-brown border-accent-brown'
                                : 'bg-white border-border-light'
                                }`}>
                                {msg.role === 'ai' ? (
                                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                                        <path d="M12 8V4H8" /><rect width="16" height="12" x="4" y="8" rx="2" /><path d="M2 14h2" /><path d="M20 14h2" /><path d="M15 13v2" /><path d="M9 13v2" />
                                    </svg>
                                ) : (
                                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#4e342e" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                                        <path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2" /><circle cx="12" cy="7" r="4" />
                                    </svg>
                                )}
                            </div>
                            <div className={`max-w-[90%] md:max-w-[85%] flex flex-col ${msg.role === 'user' ? 'items-end' : 'items-start'}`}>
                                <div className={`p-4 md:p-5 rounded-2xl md:rounded-3xl shadow-sm text-sm md:text-base leading-relaxed ${msg.role === 'user'
                                    ? 'bg-user-msg-bg text-text-primary rounded-tr-sm border border-border-light'
                                    : 'bg-white text-text-primary border border-border-light'
                                    } ${msg.isUrdu ? 'urdu-text' : ''}`}>
                                    {msg.content}
                                </div>
                                <div className="text-[10px] text-text-secondary mt-1 font-semibold uppercase tracking-wider opacity-60 group-hover:opacity-100 transition-opacity">
                                    {msg.role === 'ai' ? 'Story AI' : 'You'}
                                </div>
                            </div>
                        </div>
                    ))}
                    {isLoading && (
                        <div className="flex gap-4 md:gap-5 mb-10 w-full">
                            <div className="w-10 h-10 rounded-full bg-accent-brown flex items-center justify-center mt-1 shadow-md">
                                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M12 8V4H8" /><rect width="16" height="12" x="4" y="8" rx="2" /><path d="M2 14h2" /><path d="M20 14h2" /><path d="M15 13v2" /><path d="M9 13v2" /></svg>
                            </div>
                            <div className="flex gap-1.5 pt-6">
                                <div className="w-1.5 h-1.5 bg-accent-gold rounded-full animate-bounce [animation-delay:-0.3s]"></div>
                                <div className="w-1.5 h-1.5 bg-accent-gold rounded-full animate-bounce [animation-delay:-0.15s]"></div>
                                <div className="w-1.5 h-1.5 bg-accent-gold rounded-full animate-bounce"></div>
                            </div>
                        </div>
                    )}
                </div>
            </div>

            {/* Input */}
            <div className="p-4 md:p-6 md:pb-10 flex justify-center bg-chat-bg">
                <div className="w-full max-w-3xl relative group">
                    <textarea
                        className="w-full bg-bg-primary border border-border-light rounded-[24px] md:rounded-[32px] p-3 md:p-4 pr-14 md:pr-16 text-text-primary text-sm md:text-base outline-none resize-none focus:border-accent-gold focus:ring-2 focus:ring-accent-gold/10 transition-all min-h-[56px] md:min-h-[64px] shadow-sm hover:border-accent-gold/50"
                        rows="1"
                        placeholder="شروع کریں..."
                        value={input}
                        onChange={(e) => {
                            setInput(e.target.value);
                            e.target.style.height = 'auto';
                            e.target.style.height = e.target.scrollHeight + 'px';
                        }}
                        onKeyDown={(e) => {
                            if (e.key === 'Enter' && !e.shiftKey) {
                                e.preventDefault();
                                handleSend();
                                e.target.style.height = 'auto';
                            }
                        }}
                        style={{ direction: 'rtl' }}
                    />
                    <button
                        className="absolute right-3.5 bottom-3.5 w-11 h-11 flex items-center justify-center bg-accent-brown rounded-full disabled:opacity-30 hover:brightness-110 active:scale-90 transition-all shadow-lg shadow-accent-brown/10"
                        onClick={handleSend}
                        disabled={isLoading || !input.trim()}
                    >
                        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                            <line x1="22" y1="2" x2="11" y2="13"></line><polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
                        </svg>
                    </button>
                </div>
            </div>
        </div>
    );
};

export default ChatFeature;
