import React, { useState } from 'react';
import SidebarFeature from './features/sidebar/SidebarFeature';
import ChatFeature from './features/chat/ChatFeature';
import AuthFeature from './features/auth/AuthFeature';
import Button from './components/ui/Button';

function App() {
  const [messages, setMessages] = useState([
    {
      role: 'ai',
      content: 'ہیلو! میں آپ کے لیے اردو کہانیاں تیار کر سکتا ہوں۔ کوئی بھی شروعاتی الفاظ لکھیں (مثلاً: ایک دفعہ کا ذکر ہے)۔',
      isUrdu: true
    }
  ]);
  const [isLoading, setIsLoading] = useState(false);
  const [isSidebarOpen, setIsSidebarOpen] = useState(window.innerWidth > 768);
  const [isAuthModalOpen, setIsAuthModalOpen] = useState(false);
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [initialToggleMode, setInitialToggleMode] = useState('login');

  const onNewStory = () => {
    setMessages([messages[0]]);
    if (window.innerWidth <= 768) setIsSidebarOpen(false);
  };

  const openAuth = (mode) => {
    setInitialToggleMode(mode);
    setIsAuthModalOpen(true);
  };

  return (
    <div className="flex h-screen w-screen bg-bg-primary overflow-hidden font-sans text-text-primary">
      <AuthFeature
        isOpen={isAuthModalOpen}
        onClose={() => setIsAuthModalOpen(false)}
        onAuthSuccess={() => setIsLoggedIn(true)}
        initialMode={initialToggleMode}
      />

      {isSidebarOpen && window.innerWidth <= 768 && (
        <div
          className="mobile-overlay"
          onClick={() => setIsSidebarOpen(false)}
        />
      )}

      <SidebarFeature
        isOpen={isSidebarOpen}
        setIsOpen={setIsSidebarOpen}
        onNewStory={onNewStory}
        isLoggedIn={isLoggedIn}
        onAuthClick={openAuth}
      />

      <main className="flex-1 flex flex-col relative h-full">
        <header className="h-16 px-4 md:px-6 flex items-center justify-between bg-chat-bg/90 backdrop-blur-md sticky top-0 z-40 border-b border-border-light/50">
          <div className="flex items-center">
            <button
              className="p-2 mr-2 md:mr-4 rounded-lg text-text-secondary hover:text-text-primary hover:bg-bg-primary transition-all focus:outline-none group"
              onClick={() => setIsSidebarOpen(!isSidebarOpen)}
            >
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                {isSidebarOpen ? (
                  <><rect width="18" height="18" x="3" y="3" rx="2" /><path d="M9 3v18" /><path d="m14 9-2 3 2 3" /></>
                ) : (
                  <><line x1="3" y1="12" x2="21" y2="12" /><line x1="3" y1="6" x2="21" y2="6" /><line x1="3" y1="18" x2="21" y2="18" /></>
                )}
              </svg>
            </button>
            <div className="flex items-center gap-2 md:gap-3 overflow-visible h-full">
              <div className="w-10 h-10 md:w-12 md:h-12 rounded-full overflow-hidden border border-accent-gold/30 shadow-md bg-white shrink-0">
                <img src="/images/kaf ki khani.jpeg" alt="Logo" className="w-full h-full object-cover scale-110" />
              </div>
              <h1 className="premium-gradient-text text-lg md:text-2xl urdu-text flex items-center select-none h-full pr-4 md:pr-8 pb-1">
                کاف کی کہانی
              </h1>
            </div>
          </div>

          <div className="flex items-center gap-3">
            {!isLoggedIn ? (
              <>
                <button onClick={() => openAuth('login')} className="hidden md:block text-sm text-text-secondary hover:text-text-primary px-3 transition-colors font-semibold">Log in</button>
                <Button onClick={() => openAuth('signup')} className="text-xs px-5 py-2.5 rounded-full">Sign up free</Button>
              </>
            ) : (
              <button
                onClick={() => setIsLoggedIn(false)}
                className="w-10 h-10 rounded-full bg-accent-gold/10 border border-accent-gold/20 flex items-center justify-center cursor-pointer hover:bg-accent-gold/20 transition-all group shadow-sm"
              >
                <span className="text-xs font-bold text-accent-brown group-hover:hidden">AI</span>
                <svg className="hidden group-hover:block text-accent-brown" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" /><polyline points="16 17 21 12 16 7" /><line x1="21" y1="12" x2="9" y2="12" /></svg>
              </button>
            )}
          </div>
        </header>

        <ChatFeature
          messages={messages}
          setMessages={setMessages}
          isLoading={isLoading}
          setIsLoading={setIsLoading}
        />
      </main>
    </div>
  );
}

export default App;
