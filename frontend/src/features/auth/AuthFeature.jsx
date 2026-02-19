import React, { useState } from 'react';
import Modal from '../../components/ui/Modal';
import Button from '../../components/ui/Button';

const AuthFeature = ({ isOpen, onClose, onAuthSuccess }) => {
    const [authMode, setAuthMode] = useState('login'); // 'login' or 'signup'

    const handleAuth = (e) => {
        e.preventDefault();
        onAuthSuccess();
        onClose();
    };

    return (
        <Modal
            isOpen={isOpen}
            onClose={onClose}
            title={authMode === 'login' ? 'Welcome Back' : 'Create Account'}
        >
            <form className="space-y-4" onSubmit={handleAuth}>
                {authMode === 'signup' && (
                    <div>
                        <label className="block text-sm text-text-secondary mb-1.5 font-medium">Full Name</label>
                        <input
                            type="text"
                            className="w-full bg-bg-primary border border-border-light rounded-lg p-2.5 text-text-primary outline-none focus:border-accent-gold transition-colors"
                            placeholder="John Doe"
                            required
                        />
                    </div>
                )}
                <div>
                    <label className="block text-sm text-text-secondary mb-1.5 font-medium">Email Address</label>
                    <input
                        type="email"
                        className="w-full bg-bg-primary border border-border-light rounded-lg p-2.5 text-text-primary outline-none focus:border-accent-gold transition-colors"
                        placeholder="name@company.com"
                        required
                    />
                </div>
                <div>
                    <label className="block text-sm text-text-secondary mb-1.5 font-medium">Password</label>
                    <input
                        type="password"
                        className="w-full bg-bg-primary border border-border-light rounded-lg p-2.5 text-text-primary outline-none focus:border-accent-gold transition-colors"
                        placeholder="••••••••"
                        required
                    />
                </div>

                <Button type="submit" className="w-full py-3 mt-6">
                    {authMode === 'login' ? 'Sign In' : 'Create Account'}
                </Button>
            </form>

            <div className="mt-6 text-center text-sm text-text-secondary font-medium">
                {authMode === 'login' ? (
                    <p>Don't have an account? <button onClick={() => setAuthMode('signup')} className="text-accent-brown font-bold hover:underline">Sign up free</button></p>
                ) : (
                    <p>Already have an account? <button onClick={() => setAuthMode('login')} className="text-accent-brown font-bold hover:underline">Log in</button></p>
                )}
            </div>
        </Modal>
    );
};

export default AuthFeature;
