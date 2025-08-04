import { ethers } from "ethers";

declare global {
    interface Window {
        ethereum?: any;
    }
}

export async function connectWalletSimple() {
    if (typeof window !== "undefined" && window.ethereum) {
        try {
            const accounts = await window.ethereum.request({ method: "eth_requestAccounts" });
            const provider = new ethers.BrowserProvider(window.ethereum);
            const signer = await provider.getSigner();
            console.log("Wallet connected:", accounts[0]);
            return accounts[0]; 
        } catch (error) {
            console.error("MetaMask connectWalletSimple error:", error);
            alert("Failed to connect MetaMask. Please check your MetaMask extension.");
            return null; 
        }
    } else {
        alert("Please install MetaMask to use this feature!");
        console.error("MetaMask is not installed or window.ethereum is not available.");
        return null; 
    }
}

export async function connectMetamask() {
    if (window.ethereum) {
        try {
            const accounts = await window.ethereum.request({ method: 'eth_requestAccounts' });
            return accounts[0];
        } catch (err) {
            console.error("MetaMask connectMetamask error:", err);
            throw err;
        }
    } else {
        throw new Error('MetaMask not installed');
    }
}