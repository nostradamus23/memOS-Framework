'use client'

import * as React from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { MemeService } from "@/app/services/memeService"
import { CharacterCard } from "@/components/character-card"
import { useState, useEffect } from 'react';
import { ChatMessage } from "@/components/chat-message"
import { Twitter, BookOpen, Send, Copy, Check } from "lucide-react"

interface CharacterAnalysis {
  name: string;
  appearanceTraits: string[];
  possibleJokes: string[];
  personality: string;
}

interface ErrorWithMessage {
  message: string;
}

function isErrorWithMessage(error: unknown): error is ErrorWithMessage {
  return (
    typeof error === 'object' &&
    error !== null &&
    'message' in error &&
    typeof (error as Record<string, unknown>).message === 'string'
  );
}

function getErrorMessage(error: unknown) {
  if (isErrorWithMessage(error)) return error.message;
  return 'Something went wrong';
}

export function MemeTerminal() {
  const [input, setInput] = React.useState("")
  const [output, setOutput] = React.useState<(string | {
    speaker: string;
    message: string;
    imageUrl?: string;
  })[]>([])
  const [file, setFile] = React.useState<File | null>(null)
  const [isAIMode, setIsAIMode] = React.useState(false)
  const [isDragging, setIsDragging] = React.useState(false)
  const [isLoading, setIsLoading] = React.useState(false)
  const [memeService] = React.useState(() => new MemeService())
  const [analysis, setAnalysis] = React.useState<CharacterAnalysis | null>(null);
  const [imageUrl, setImageUrl] = React.useState<string>('');
  const chatContainerRef = React.useRef<HTMLDivElement>(null);
  const [sessionId, setSessionId] = useState<string>('');
  const [copied, setCopied] = React.useState(false);

  useEffect(() => {
    // Crear o recuperar sessionId al montar el componente
    const existingSessionId = localStorage.getItem('sessionId');
    if (existingSessionId) {
      setSessionId(existingSessionId);
    } else {
      fetch('/api/session/create')
        .then(res => res.json())
        .then(data => {
          setSessionId(data.sessionId);
          localStorage.setItem('sessionId', data.sessionId);
        });
    }
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [output]);

  const scrollToBottom = () => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file || !input) return;
    setIsLoading(true);

    try {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('memeName', input);
      formData.append('sessionId', sessionId);

      const description = await memeService.analizarImagen(formData);
      setAnalysis(description.analysis);
      setImageUrl(URL.createObjectURL(file));
      
      setOutput([
        `> Character analysis complete`,
        "> Starting conversation..."
      ]);

      setTimeout(async () => {
        try {
          const initialMessage = await memeService.sendDirectMessage("Hello! Please introduce yourself and tell me about your personality.");
          setOutput(prev => [...prev, {
            speaker: description.analysis.name,
            message: initialMessage,
            imageUrl: URL.createObjectURL(file)
          }]);
        } catch (error: unknown) {
          setOutput(prev => [...prev, `> Error: ${getErrorMessage(error)}`]);
        }
      }, 1000);

      setInput("");
      setIsAIMode(true);
    } catch (error: unknown) {
      setOutput(prev => [...prev, `> Error: ${getErrorMessage(error)}`]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (file) {
      setOutput([...output, "> Error: An image is already uploaded. Please submit or clear the current image first."])
      return
    }
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0])
    }
  }

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(true)
  }

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(false)
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(false)
    
    if (file) {
      setOutput([...output, "> Error: An image is already uploaded. Please submit or clear the current image first."])
      return
    }
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setFile(e.dataTransfer.files[0])
      setOutput([...output, `> Loaded image: ${e.dataTransfer.files[0].name}`])
    }
  }

  const handleClear = () => {
    setFile(null)
    setInput("")
    setOutput([])
    setIsAIMode(false)
  }

  const handleCopy = async () => {
    await navigator.clipboard.writeText("So11111111111111111111111111111111111111112");
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleChat = async () => {
    if (!input) return;
    setIsLoading(true);
    try {
      setOutput(prev => [...prev, {
        speaker: 'User',
        message: input
      }]);
      const response = await memeService.sendDirectMessage(input);
      setOutput(prev => [...prev, {
        speaker: analysis?.name || '',
        message: response,
        imageUrl: imageUrl
      }]);
    } catch (error: unknown) {
      setOutput(prev => [...prev, `> Error: ${getErrorMessage(error)}`]);
    } finally {
      setIsLoading(false);
    }
    setInput('');
  };

  return (
    <div className="h-screen flex flex-col bg-black overflow-hidden">
      {/* Header */}
      <header className="border-b border-green-400 p-4 flex-shrink-0">
        <div className="max-w-7xl mx-auto flex justify-between items-center">
          <div className="flex items-center gap-2">
            <a href="/" className="text-green-400 text-xl font-mono hover:text-green-300 transition-colors">
              memOS
            </a>
          </div>
          <nav className="flex items-center gap-4">
            <a href="https://x.com/memOSai_" target="_blank" rel="noopener noreferrer" className="text-green-400 hover:text-green-300 transition-colors">
              <Twitter size={20} />
            </a>
            <a href="https://docs.memosai.org/memos-docs" className="text-green-400 hover:text-green-300 transition-colors">
              <BookOpen size={20} />
            </a>
            <a href="https://t.me/memosportal" target="_blank" rel="noopener noreferrer" className="text-green-400 hover:text-green-300 transition-colors">
              <Send size={20} />
            </a>
          </nav>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 flex gap-4 p-4 min-h-0 mt-4">
        <div className="flex-1">
          <div className="h-full bg-black text-green-400 font-mono flex items-center justify-center">
            <div className="w-full max-w-2xl">
              <div className="mb-4">
                <div className="flex justify-between items-center">
                  <p className="text-3xl">memOS v1.0</p>
                </div>
              </div>
              <div className="relative">
                <div 
                  ref={chatContainerRef}
                  className={`bg-black border border-green-400 p-4 h-[calc(100vh-20rem)] overflow-y-auto mb-4 relative ${
                    isDragging ? 'border-dashed border-2' : ''
                  }`}
                  onDragOver={handleDragOver}
                  onDragLeave={handleDragLeave}
                  onDrop={handleDrop}
                >
                  <Button 
                    type="button" 
                    onClick={handleClear}
                    className="absolute top-2 right-2 bg-green-400 text-black hover:bg-green-500 z-10"
                  >
                    Clear
                  </Button>
                  {output.length === 0 && (
                    <>
                      <Input
                        type="file"
                        onChange={handleFileChange}
                        className="absolute inset-0 opacity-0 w-full h-full cursor-pointer z-10"
                        accept="image/*"
                      />
                      <div className="absolute inset-0 flex flex-col items-center justify-center text-green-400 opacity-50 space-y-2">
                        <div className="text-lg">Drop your meme image here</div>
                        <div className="text-sm">or click to select a file</div>
                        <div className="mt-4 text-xs opacity-75">👆 Then enter his name</div>
                      </div>
                    </>
                  )}
                  {output.map((line, index) => {
                    if (typeof line === 'string') {
                      return <p key={index} className="text-green-400 mb-1">{line}</p>;
                    }
                    return (
                      <ChatMessage
                        key={index}
                        speaker={line.speaker}
                        message={line.message}
                        imageUrl={line.imageUrl}
                      />
                    );
                  })}
                </div>
              </div>
              <form onSubmit={handleSubmit} className="flex flex-col space-y-2">
                {isAIMode ? (
                  <div className="space-y-2">
                    <Input
                      type="text"
                      value={input}
                      onChange={(e) => setInput(e.target.value)}
                      onKeyDown={(e) => {
                        if (e.key === 'Enter' && !e.shiftKey) {
                          e.preventDefault();
                          if (input.trim()) {
                            handleChat();
                          }
                        }
                      }}
                      placeholder="Enter a topic or message..."
                      className="bg-black text-green-400 border-green-400 focus:ring-green-400 focus:border-green-400 h-10"
                    />
                    <div className="space-y-2">
                      <Button
                        type="button"
                        onClick={handleChat}
                        className="w-full bg-green-400 text-black hover:bg-green-500"
                        disabled={isLoading || !input}
                      >
                        Chat with {analysis?.name}
                      </Button>
                      <div className="flex justify-center items-center gap-2 text-green-400 font-mono text-sm">
                        <span>ca:</span>
                        <button
                          onClick={handleCopy}
                          className="flex items-center gap-2 hover:text-green-300 transition-colors focus:outline-none"
                        >
                          <span className="font-mono">So11111111111111111111111111111111111111112</span>
                          {copied ? <Check size={16} /> : <Copy size={16} />}
                        </button>
                      </div>
                    </div>
                  </div>
                ) : (
                  <>
                    <div className="grid grid-cols-2 gap-2">
                      <div className="relative">
                        <Input
                          type="file"
                          onChange={handleFileChange}
                          className="absolute inset-0 opacity-0 w-full h-full cursor-pointer"
                          accept="image/*"
                        />
                        <div className="bg-black text-green-400 border border-green-400 rounded-md px-3 py-2 h-10 w-full truncate">
                          {file ? file.name : "Select a file"}
                        </div>
                      </div>
                      <div className="relative">
                        <Input
                          type="text"
                          value={input}
                          onChange={(e) => setInput(e.target.value)}
                          placeholder="Name"
                          className="bg-black text-green-400 border-green-400 focus:ring-green-400 focus:border-green-400 h-10"
                        />
                        <div className="absolute -right-40 top-1/2 -translate-y-1/2 flex items-center gap-2 text-green-400 text-sm opacity-75">
                          <span>👈</span>
                          <span>enter the name</span>
                        </div>
                      </div>
                    </div>
                    <div className="space-y-2">
                      <Button 
                        type="submit" 
                        className="w-full bg-green-400 text-black hover:bg-green-500"
                        disabled={isLoading || !file || !input}
                      >
                        {isLoading ? "Processing..." : "Analyze Character"}
                      </Button>
                      <div className="flex justify-center items-center gap-2 text-green-400 font-mono text-sm">
                        <span>ca:</span>
                        <button
                          onClick={handleCopy}
                          className="flex items-center gap-2 hover:text-green-300 transition-colors focus:outline-none"
                        >
                          <span className="font-mono">So11111111111111111111111111111111111111112</span>
                          {copied ? <Check size={16} /> : <Copy size={16} />}
                        </button>
                      </div>
                    </div>
                  </>
                )}
              </form>
            </div>
          </div>
        </div>
        
        {analysis && (
          <div className="w-80 p-4 bg-black border border-green-400 text-green-400 font-mono overflow-y-auto">
            <h2 className="text-lg mb-4">Character Analysis</h2>
            <p className="mb-2">Name: {analysis.name}</p>
            <div className="mb-2">
              <p>Appearance:</p>
              <ul className="list-disc pl-4">
                {analysis.appearanceTraits.map((trait, i) => (
                  <li key={i}>{trait}</li>
                ))}
              </ul>
            </div>
            <div className="mb-2">
              <p>Jokes:</p>
              <ul className="list-disc pl-4">
                {analysis.possibleJokes.map((joke, i) => (
                  <li key={i}>{joke}</li>
                ))}
              </ul>
            </div>
            <p>Personality: {analysis.personality}</p>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="border-t border-green-400 p-4 flex-shrink-0">
        <div className="max-w-7xl mx-auto flex justify-between items-center text-green-400 font-mono text-sm">
          <p>© 2024 memOS. All rights reserved.</p>
          <div className="flex items-center gap-4">
            <a href="https://x.com/memOSai_" target="_blank" rel="noopener noreferrer" className="text-green-400 hover:text-green-300 transition-colors">
              <Twitter size={20} />
            </a>
            <a href="https://docs.memosai.org/memos-docs" target="_blank" rel="noopener noreferrer" className="text-green-400 hover:text-green-300 transition-colors">
              <BookOpen size={20} />
            </a>
            <a href="https://t.me/memosportal" target="_blank" rel="noopener noreferrer" className="text-green-400 hover:text-green-300 transition-colors">
              <Send size={20} />
            </a>
          </div>
        </div>
      </footer>
    </div>
  )
}