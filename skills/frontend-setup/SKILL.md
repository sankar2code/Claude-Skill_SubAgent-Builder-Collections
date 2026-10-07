---
name: frontend-setup
description: >
  Scaffolds a complete Next.js 16 (App Router) project with TypeScript by writing all
  necessary files, creates a styled landing page, and runs the app end to end.
  Use this skill whenever the user asks to:
  - Set up a Next.js project or folder structure
  - Bootstrap a Next.js environment with all dependencies
  - Get a Next.js landing page up and running
  - Start a new Next.js project (even casually, e.g. "let's set up Next.js" or "new Next app")
  Trigger this skill immediately when the user mentions Next.js setup or starting
  a Next.js project, even if they say it casually like "let's set up Next".
  Stage 4 of the PRD → Production pack.
---

> **PRD → Production pack · Stage 4 of 5.** `engineering-planner` → `implementation-specs` → `security-foundation` → `frontend-setup` → build features (with `design-system` always on)
> Stop after this stage, show the user what was produced, and wait for approval before moving on.

# Next.js Setup Skill

Your job is to scaffold a complete Next.js 16 (App Router) project end to end by writing all files manually, then starting the dev server.

**Default stack: Next.js 16 + React 19 + TypeScript.** If the PRD or engineering doc specifies a different stack, confirm with the user before using it. Never switch stacks silently.

Do every step in order. Do not skip any step.

---

## Step 1 — Check the engineering doc for stack overrides

Before asking the user anything, read `docs/engineering/engineering-doc.md` (and `docs/specs/` if present) if they exist. Look for:
- Framework preference (Next.js version, Remix, Vite, etc.)
- Language preference (TypeScript vs JavaScript)
- Any additional dependencies called out (UI library, state management, etc.)
- The folder structure and naming conventions the specs define

Then follow this decision tree:

**If the docs specify a different tech stack** (e.g. JavaScript instead of TypeScript, Vite instead of Next.js):
- Ask the user to confirm before proceeding:
  - **Question:** "The PRD specifies [X]. Would you like to use that, or stick with the default (Next.js 16 + TypeScript)?"
  - **Options:** "Use [X] from the PRD" / "Use the default (Next.js 16 + TypeScript)"
- Use whichever option the user picks and apply it throughout the steps below.

**If the docs are silent or don't exist:**
- Use the defaults: **Next.js 16, React 19, TypeScript**. No need to ask about the stack.

---

## Step 2 — Ask the user about the project folder

Ask the user:

**Question:** "Where would you like to set up the Next.js project?"
**Options:**
- **Create a new folder**: scaffold a fresh `nextjs-app` folder (recommended for a clean start)
- **Use an existing folder**: work inside a folder the user already has; ask them for the path

---

## Step 3 — Set up the project folder

- **New folder:** create `nextjs-app/` and `nextjs-app/app/` in the current working directory.
- **Existing folder:** use the path they gave; create an `app/` subfolder if it doesn't exist. Before writing, list any of the files below that already exist there and ask the user whether to overwrite them. **Never delete the folder or any file the user didn't approve.**

If the specs define a folder structure (for example `lib/`, `components/`, `lib/security/`), create those empty folders too.

---

## Step 4 — Write `package.json`

```json
{
  "name": "nextjs-app",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start"
  },
  "dependencies": {
    "next": "^16.4.0",
    "react": "^19.3.0",
    "react-dom": "^19.3.0"
  },
  "devDependencies": {
    "@types/node": "^24",
    "@types/react": "^19",
    "@types/react-dom": "^19",
    "typescript": "^5"
  }
}
```

Note: `next lint` was removed in Next.js 16. If the project needs linting, add ESLint directly (`eslint` + `eslint-config-next`) with its own `lint` script.

---

## Step 5 — Write `tsconfig.json`

```json
{
  "compilerOptions": {
    "target": "ES2017",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "react-jsx",
    "incremental": true,
    "plugins": [{ "name": "next" }],
    "paths": {
      "@/*": ["./*"]
    }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts", ".next/dev/types/**/*.ts"],
  "exclude": ["node_modules"]
}
```

---

## Step 6 — Write `next.config.ts`

```ts
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {}

export default nextConfig
```

---

## Step 7 — Write `app/layout.tsx`

Global CSS is imported once, here in the root layout.

```tsx
import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Next.js App',
  description: 'Built with the Next.js App Router',
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
```

---

## Step 8 — Write `app/globals.css`

Include hover classes here so `page.tsx` never needs JS event handlers (which break in Server Components). If `docs/design.md` exists, use its tokens instead of the colors below (see the `design-system` skill).

```css
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.btn-primary {
  padding: 0.75rem 2rem;
  border-radius: 999px;
  background: #00c6ff;
  color: #0f0c29;
  font-weight: 700;
  font-size: 1rem;
  text-decoration: none;
  display: inline-block;
  transition: transform 0.2s;
}
.btn-primary:hover { transform: scale(1.05); }

.btn-ghost {
  padding: 0.75rem 2rem;
  border-radius: 999px;
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.4);
  color: #ffffff;
  font-weight: 600;
  font-size: 1rem;
  text-decoration: none;
  display: inline-block;
  transition: border-color 0.2s;
}
.btn-ghost:hover { border-color: rgba(255, 255, 255, 0.9); }
```

---

## Step 9 — Write `app/page.tsx` (the landing page)

> **IMPORTANT — Server Component rule:** `app/page.tsx` is a React Server Component by default.
> Never use `onMouseOver`, `onMouseOut`, `onClick`, or any other JS event handler props on elements here.
> Those props are only valid in Client Components (`'use client'`).
> Use CSS classes from `globals.css` for all hover and interactive effects instead.

```tsx
export default function Home() {
  return (
    <main style={{
      minHeight: '100vh',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      background: 'linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%)',
      color: '#ffffff',
      textAlign: 'center',
      padding: '2rem',
    }}>
      <h1 style={{
        fontSize: '3.5rem',
        fontWeight: 800,
        marginBottom: '1rem',
        background: 'linear-gradient(90deg, #00c6ff, #a78bfa)',
        WebkitBackgroundClip: 'text',
        WebkitTextFillColor: 'transparent',
      }}>
        Hello, Next.js
      </h1>
      <p style={{
        fontSize: '1.25rem',
        color: '#a8b2d8',
        maxWidth: '520px',
        lineHeight: 1.8,
        marginBottom: '2rem',
      }}>
        Your Next.js 16 app is up and running with the App Router and TypeScript. Let's build something amazing.
      </p>
      <a
        href="https://nextjs.org/docs"
        target="_blank"
        rel="noopener noreferrer"
        className="btn-primary"
      >
        Read the Docs
      </a>
    </main>
  )
}
```

---

## Step 10 — Show the final folder structure

Tell the user what was created:

```
nextjs-app/
├── next.config.ts
├── package.json
├── tsconfig.json
└── app/
    ├── layout.tsx      ← root layout (metadata, html/body tags, global CSS)
    ├── globals.css     ← global styles
    └── page.tsx        ← your landing page
```

---

## Step 11 — Run the app (end to end)

Install, then start the dev server in the background:

```bash
cd <project-path> && npm install
(npm run dev -- --port 3000 > /tmp/nextjs-app.log 2>&1 &)
sleep 8 && cat /tmp/nextjs-app.log
```

**If the server starts successfully**, tell the user:
> Your Next.js app is live at **http://localhost:3000**. Open it in your browser!

**If npm is blocked or the server fails**, give the user these commands to run in their own terminal:

```bash
cd nextjs-app
npm install && npm run dev
```

Then tell them:
> Once it starts, open **http://localhost:3000** in your browser to see the landing page.

---

## When done

Ask:
> "Your Next.js app is scaffolded and running. Let me know when you're ready to start building features from `docs/specs/`. I'll build one feature at a time, with the `design-system` skill applied to all UI."

---

## Notes

- Requires **Node.js 20.9 or later** (Next.js 16 minimum).
- **TypeScript by default.** Use `.tsx` / `.ts` unless the user confirmed a JavaScript stack in Step 1.
- Replace `<project-path>` with the actual absolute path to the project directory.
- Port 3000 is Next.js's default. If it's in use, try 3001.
- This scaffold uses the **App Router** (`app/` directory). Do NOT use the old `pages/` directory unless the user explicitly asks.
- Next.js 16 uses Turbopack by default for `dev` and `build`. No extra config is needed.
- Route protection lives in `proxy.ts` on Next.js 16 (it was `middleware.ts` before). The `security-foundation` skill creates it.
- Do NOT explain every file in detail. Confirm each one was written, then move on.
- **NEVER use JS event handler props (`onMouseOver`, `onMouseOut`, `onClick`, etc.) in `app/page.tsx` or any other Server Component.** App Router files are Server Components by default, and passing event handlers to them throws an error: _"Event handlers cannot be passed to Client Component props."_ Use CSS classes from `globals.css` for hover and interactive effects. Only add `'use client'` at the top of a file when the component genuinely needs React state, effects, or browser event handlers.
