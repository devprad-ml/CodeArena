import Editor from '@monaco-editor/react'
import { useArenaStore } from '@/store/arenaStore'
import { SUPPORTED_LANGUAGES } from '@/utils/constants'
import { CODE_TEMPLATES } from '@/utils/codeTemplates'

export default function CodeEditor() {
  const { code, setCode, language } = useArenaStore()

  const monacoLang = SUPPORTED_LANGUAGES.find((l) => l.id === language)?.monacoLang ?? 'python'

  const handleMount = (_editor, monaco) => {
    monaco.editor.defineTheme('codearena-dark', {
      base: 'vs-dark',
      inherit: true,
      rules: [],
      colors: {
        'editor.background': '#0d0d0d',
        'editor.lineHighlightBackground': '#1a1a1a',
        'editorLineNumber.foreground': '#444444',
        'editorGutter.background': '#0d0d0d',
      },
    })
    monaco.editor.setTheme('codearena-dark')
  }

  return (
    <Editor
      height="100%"
      language={monacoLang}
      value={code || CODE_TEMPLATES[language] || ''}
      onChange={(val) => setCode(val ?? '')}
      onMount={handleMount}
      options={{
        fontSize: 14,
        fontFamily: '"JetBrains Mono", "Fira Code", monospace',
        fontLigatures: true,
        minimap: { enabled: false },
        scrollBeyondLastLine: false,
        wordWrap: 'on',
        lineNumbers: 'on',
        renderLineHighlight: 'line',
        tabSize: 4,
        automaticLayout: true,
        padding: { top: 12 },
      }}
    />
  )
}
