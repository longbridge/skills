#!/usr/bin/env bun
/**
 * Generate skills.json from all skills/<slug>/SKILL.md frontmatter.
 * Usage: bun run scripts/build-skills-json.ts [--output PATH]
 */
import { readdirSync } from "fs"
import { join } from "path"

const REPO_ROOT = join(import.meta.dir, "..")
const SKILLS_DIR = join(REPO_ROOT, "skills")

interface SkillEntry {
  slug: string
  name: string
  description: string
  metadata: Record<string, unknown>
}

function parseFrontmatter(content: string): Record<string, unknown> | null {
  if (!content.startsWith("---\n")) return null
  const end = content.indexOf("\n---\n", 4)
  if (end === -1) return null
  return parseYaml(content.slice(4, end))
}

function parseYaml(text: string): Record<string, unknown> {
  const result: Record<string, unknown> = {}
  const lines = text.split("\n")
  let i = 0

  while (i < lines.length) {
    const line = lines[i]
    if (!line.trim() || line.startsWith("#")) { i++; continue }

    const m = line.match(/^([a-zA-Z_][a-zA-Z0-9_-]*):\s*(.*)$/)
    if (!m) { i++; continue }

    const [, key, rest] = m
    i++

    if (rest.trimEnd() === "|") {
      const buf: string[] = []
      while (i < lines.length && (lines[i].startsWith("  ") || lines[i] === "")) {
        buf.push(lines[i].startsWith("  ") ? lines[i].slice(2) : "")
        i++
      }
      result[key] = buf.join("\n").trimEnd()
    } else if (rest.trimEnd() === ">") {
      const buf: string[] = []
      while (i < lines.length && (lines[i].startsWith("  ") || lines[i] === "")) {
        buf.push(lines[i].startsWith("  ") ? lines[i].slice(2) : "")
        i++
      }
      // Folded scalar: join lines with spaces, blank lines become newlines
      const folded: string[] = []
      let chunk: string[] = []
      for (const ln of buf) {
        if (ln === "") {
          if (chunk.length) { folded.push(chunk.join(" ")); chunk = [] }
          folded.push("")
        } else {
          chunk.push(ln)
        }
      }
      if (chunk.length) folded.push(chunk.join(" "))
      result[key] = folded.join("\n").trimEnd()
    } else if (rest === "") {
      const obj: Record<string, unknown> = {}
      while (i < lines.length && lines[i].startsWith("  ")) {
        const nm = lines[i].trim().match(/^([a-zA-Z_][a-zA-Z0-9_-]*):\s*(.+)$/)
        if (nm) {
          const v = nm[2].trim().replace(/^["']|["']$/g, "")
          obj[nm[1]] = v === "true" ? true : v === "false" ? false : v
        }
        i++
      }
      result[key] = obj
    } else {
      result[key] = rest.trim().replace(/^["']|["']$/g, "")
    }
  }

  return result
}

const outputFlag = process.argv.indexOf("--output")
const outputPath =
  outputFlag !== -1 && outputFlag + 1 < process.argv.length
    ? process.argv[outputFlag + 1]
    : join(REPO_ROOT, "skills.json")

const skills: SkillEntry[] = []
let errors = 0

for (const entry of readdirSync(SKILLS_DIR, { withFileTypes: true }).sort((a, b) =>
  a.name.localeCompare(b.name),
)) {
  if (!entry.isDirectory()) continue
  const skillMdPath = join(SKILLS_DIR, entry.name, "SKILL.md")
  const file = Bun.file(skillMdPath)
  if (!(await file.exists())) continue

  try {
    const fm = parseFrontmatter(await file.text())
    if (!fm) continue
    skills.push({
      slug: entry.name,
      name: (fm.name as string) ?? entry.name,
      description: ((fm.description as string) ?? "").trim(),
      metadata: (fm.metadata as Record<string, unknown>) ?? {},
    })
  } catch (err) {
    console.error(`Warning: failed to parse ${skillMdPath}:`, err)
    errors++
  }
}

const output = {
  version: "1.0",
  skills,
}

await Bun.write(outputPath, JSON.stringify(output, null, 2) + "\n")
console.log(`Generated ${outputPath} with ${skills.length} skills (${errors} errors)`)
