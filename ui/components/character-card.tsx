import Image from 'next/image';

interface CharacterAnalysis {
  name: string;
  appearanceTraits: string[];
  possibleJokes: string[];
  personality: string;
}

interface CharacterCardProps {
  analysis: CharacterAnalysis;
  imageUrl: string;
}

export function CharacterCard({ analysis, imageUrl }: CharacterCardProps) {
  return (
    <div className="bg-black border border-green-400 rounded-lg p-4 w-80">
      <div className="mb-4 relative h-48">
        <Image 
          src={imageUrl} 
          alt={analysis.name}
          fill
          className="object-cover rounded border border-green-400"
        />
      </div>
      
      <div className="space-y-4 text-green-400">
        <div>
          <h3 className="text-lg font-bold mb-1">Name:</h3>
          <p>{analysis.name}</p>
        </div>
        
        <div>
          <h3 className="text-lg font-bold mb-1">Appearance Traits:</h3>
          <ul className="list-disc list-inside">
            {analysis.appearanceTraits.map((trait, index) => (
              <li key={index}>{trait}</li>
            ))}
          </ul>
        </div>
        
        <div>
          <h3 className="text-lg font-bold mb-1">Possible Jokes:</h3>
          <ul className="list-disc list-inside">
            {analysis.possibleJokes.map((joke, index) => (
              <li key={index}>{joke}</li>
            ))}
          </ul>
        </div>
        
        <div>
          <h3 className="text-lg font-bold mb-1">Personality:</h3>
          <p>{analysis.personality}</p>
        </div>
      </div>
    </div>
  );
} 