import React from 'react';
import Button from '../../components/ui/Button';

const SidebarFeature = ({ isOpen, onNewStory, isLoggedIn, onAuthClick }) => {
    return (
        <aside
            className={`sidebar-transition flex flex-col bg-sidebar-bg overflow-hidden z-50 ${isOpen ? 'w-[260px] p-3 opacity-100' : 'w-0 p-0 opacity-0'
                }`}
        >
            <button
                className="flex items-center gap-3 w-full p-2.5 mb-6 border border-border-light bg-white rounded-lg text-text-primary hover:bg-bg-primary transition-all font-semibold whitespace-nowrap shadow-sm"
                onClick={onNewStory}
            >
                <span className="text-lg bg-accent-gold/20 text-accent-brown w-6 h-6 flex items-center justify-center rounded-md">+</span>
                <span>New Story</span>
            </button>

            <div className="flex-1 overflow-y-auto space-y-1">
                <div className="text-[11px] font-bold text-text-secondary uppercase tracking-widest px-2 mb-2">History</div>
                <div className="p-2.5 rounded-lg cursor-pointer text-sm text-text-secondary hover:bg-white hover:text-text-primary hover:shadow-sm transition-all truncate">Yesterday's Story</div>
                <div className="p-2.5 rounded-lg cursor-pointer text-sm text-text-secondary hover:bg-white hover:text-text-primary hover:shadow-sm transition-all truncate">Lion and the Mouse</div>
            </div>

            {!isLoggedIn && (
                <div className="mt-auto p-4 space-y-2">
                    <button
                        onClick={() => onAuthClick('login')}
                        className="w-full py-2 text-sm text-text-secondary hover:text-text-primary font-medium transition-colors"
                    >
                        Log in
                    </button>
                    <Button
                        onClick={() => onAuthClick('signup')}
                        className="w-full py-2.5 text-sm rounded-xl"
                    >
                        Sign up free
                    </Button>
                </div>
            )}
        </aside>
    );
};

export default SidebarFeature;
