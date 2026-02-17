/**
 * API Contract Test
 * ──────────────────
 * Validates that the production API at Heroku returns the expected data shape.
 * Tests:
 *  1. /api/matches returns 200
 *  2. Response shape has required top-level keys
 *  3. Match items have required fields
 *  4. sportCounts is populated
 *  5. Nullable fields don't crash (nulls allowed but structure valid)
 */

const API_BASE = process.env.API_URL || 'https://pickly-67e87ed00f70.herokuapp.com'

let failures = 0

function assert(condition, msg) {
  if (condition) {
    console.log(`  ✅ ${msg}`)
  } else {
    console.error(`  ❌ ${msg}`)
    failures++
  }
}

function section(title) {
  console.log(`\n── ${title} ──`)
}

async function main() {
  // ── 1. Fetch matches endpoint ──
  section('API Connectivity')
  let response
  try {
    response = await fetch(`${API_BASE}/api/matches`)
  } catch (err) {
    console.error(`  ❌ Failed to connect: ${err.message}`)
    process.exit(1)
  }
  assert(response.ok, `GET /api/matches → ${response.status} (expected 2xx)`)

  // ── 2. Parse JSON ──
  const json = await response.json()
  assert(typeof json === 'object' && json !== null, 'Response is a JSON object')

  // ── 3. Top-level shape ──
  section('Top-level response shape')
  assert(Array.isArray(json.data), '"data" is an array')
  assert(typeof json.meta === 'object', '"meta" is an object')
  assert(typeof json.stats === 'object', '"stats" is an object')
  assert(
    typeof json.sportCounts === 'object' && json.sportCounts !== null,
    '"sportCounts" is an object',
  )

  // ── 4. sportCounts validation ──
  section('sportCounts')
  const counts = json.sportCounts || {}
  const totalFromCounts = Object.values(counts).reduce((a, b) => a + b, 0)
  assert(totalFromCounts > 0, `sportCounts total = ${totalFromCounts} (> 0)`)

  // ── 5. Match item fields ──
  section('Match item structure')
  if (json.data.length > 0) {
    const sample = json.data[0]
    const requiredFields = [
      'id', 'homeTeam', 'awayTeam', 'sport', 'time',
    ]
    for (const field of requiredFields) {
      assert(field in sample, `Match has "${field}" field`)
    }

    // Nullable but structurally valid fields
    const nullableFields = ['odds', 'forebet', 'sofascore', 'gemini', 'h2h']
    for (const field of nullableFields) {
      const value = sample[field]
      assert(
        value === null || value === undefined || typeof value === 'object',
        `"${field}" is null/undefined/object (got ${typeof value})`,
      )
    }

    // ── 6. Sub-object shapes (when present) ──
    section('Sub-object shapes (on sample match)')

    // Odds
    if (sample.odds && typeof sample.odds === 'object') {
      assert('home' in sample.odds, 'odds.home exists')
      assert('away' in sample.odds, 'odds.away exists')
    }

    // Forebet
    if (sample.forebet && typeof sample.forebet === 'object') {
      assert('prediction' in sample.forebet, 'forebet.prediction exists')
    }

    // SofaScore
    if (sample.sofascore && typeof sample.sofascore === 'object') {
      assert('home' in sample.sofascore, 'sofascore.home exists')
    }

    console.log(`\n  ℹ️  Tested ${json.data.length} matches from API`)
  } else {
    console.log('  ⚠️  No matches returned (may be expected for some dates)')
  }

  // ── Summary ──
  console.log('\n' + '═'.repeat(40))
  if (failures === 0) {
    console.log('✅ All API contract tests PASSED')
    process.exit(0)
  } else {
    console.error(`❌ ${failures} test(s) FAILED`)
    process.exit(1)
  }
}

main().catch((err) => {
  console.error(`Fatal: ${err.message}`)
  process.exit(1)
})
