import React from 'react';

const Button = ({
    children,
    onClick,
    variant = 'primary',
    className = '',
    disabled = false,
    type = 'button'
}) => {
    const baseStyles = "transition-all active:scale-95 disabled:opacity-30 font-semibold flex items-center justify-center";

    const variants = {
        primary: "bg-accent-brown text-white hover:brightness-110 shadow-lg shadow-accent-brown/15",
        secondary: "bg-white border border-border-light text-text-primary hover:bg-bg-primary shadow-sm",
        ghost: "text-text-secondary hover:text-text-primary transition-colors",
        outline: "border border-accent-gold/20 text-accent-brown hover:bg-accent-gold/10 shadow-sm"
    };

    return (
        <button
            type={type}
            onClick={onClick}
            disabled={disabled}
            className={`${baseStyles} ${variants[variant]} ${className}`}
        >
            {children}
        </button>
    );
};

export default Button;
