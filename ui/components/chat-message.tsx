import Image from 'next/image';

interface ChatMessageProps {
  speaker: string;
  message: string;
  imageUrl?: string;
}

export function ChatMessage({ speaker, message, imageUrl }: ChatMessageProps) {
  if (speaker === 'User') {
    return (
      <div className="flex items-start gap-2 mb-4">
        <div className="flex-1">
          <span className="text-xs text-green-500">{speaker}</span>
          <p className="leading-relaxed">{message}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex items-start gap-2 mb-4">
      {imageUrl && (
        <div className="w-8 h-8 flex-shrink-0 rounded-full overflow-hidden">
          <Image
            src={imageUrl}
            alt={speaker}
            width={32}
            height={32}
            className="object-cover"
          />
        </div>
      )}
      <div className="flex-1">
        <span className="text-xs text-green-500">{speaker}</span>
        <p className="leading-relaxed">{message}</p>
      </div>
    </div>
  );
} 