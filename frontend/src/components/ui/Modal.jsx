import React from 'react';

const Modal = ({ isOpen, onClose, title, children }) => {
    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 z-[100] flex items-center justify-center bg-accent-brown/20 backdrop-blur-sm p-4 animate-in fade-in duration-200">
            <div className="bg-white border border-border-light w-full max-w-md rounded-2xl p-8 shadow-2xl animate-in zoom-in duration-200">
                <div className="flex justify-between items-center mb-6">
                    <h2 className="text-2xl font-bold bg-gradient-to-r from-accent-brown to-accent-gold bg-clip-text text-transparent">
                        {title}
                    </h2>
                    <button onClick={onClose} className="text-text-secondary hover:text-text-primary transition-colors">
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                            <path d="M18 6 6 18" /><path d="m6 6 12 12" />
                        </svg>
                    </button>
                </div>
                {children}
            </div>
        </div>
    );
};

export default Modal;
