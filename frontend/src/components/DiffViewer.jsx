import React, { useMemo } from 'react';
import { diffLines } from 'diff';

export default function DiffViewer({ oldCode, newCode }) {
  const diffResult = useMemo(() => {
    // Clean up both snippets for comparison
    const cleanOld = (oldCode || '').trim();
    const cleanNew = (newCode || '').trim();
    return diffLines(cleanOld, cleanNew);
  }, [oldCode, newCode]);

  let lineNum = 1;

  return (
    <div className="diff-viewer">
      {diffResult.map((part, partIdx) => {
        const lines = part.value.split('\n').filter((l, i, arr) => {
          // Remove trailing empty line from split
          return !(i === arr.length - 1 && l === '');
        });

        return lines.map((line, lineIdx) => {
          const key = `${partIdx}-${lineIdx}`;
          let className = 'diff-line';
          let prefix = ' ';

          if (part.added) {
            className += ' diff-added';
            prefix = '+';
          } else if (part.removed) {
            className += ' diff-removed';
            prefix = '-';
          }

          const currentLine = part.removed ? '' : lineNum++;
          if (part.added) {
            // Don't increment for removed lines
          }

          return (
            <div key={key} className={className}>
              <span className="diff-line-number">
                {part.removed ? '-' : currentLine || ''}
              </span>
              <span className="diff-line-prefix">{prefix}</span>
              <span className="diff-line-content">{line || ' '}</span>
            </div>
          );
        });
      })}
    </div>
  );
}
