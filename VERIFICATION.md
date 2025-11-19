---
title: GitHub - Verification Guide
type: reference
status: active
last_updated: '2025-11-14'
tags:
- documentation
- reference
---

# GitHub - Verification Guide

**Generated from**: chora-base 5.0.0 (SAP-047 Capability Server Template)
**Project**: github
**Namespace**: github
**Generated**: {{ timestamp }}

---

## Purpose

This guide enables autonomous verification of your capability server project through L1-L4 verification levels, following the comprehensive plan in chora-base.

**For Claude Code**: This document provides a self-contained verification workflow. You can execute this plan autonomously by following the sections below.

---

## Quick Verification Checklist

### L1: Configured (Basic Generation)
- [ ] All expected files generated (~80 files)
- [ ] Core layer present (models, business logic)
- [ ] Interface layers present (CLI, REST)






- [ ] Dependencies installable (`pip install -e ".[dev]"`)
- [ ] Project structure matches capability server architecture

### L2: Usage (Comprehensive Testing)
- [ ] **Quality Gates**: All pass
  - [ ] Ruff linting: `ruff check .` (0 errors)
  - [ ] Ruff formatting: `ruff format --check .` (0 errors)
  - [ ] Mypy type checking: `mypy github` (0 errors)
  - [ ] Pytest tests: `pytest` (all pass)
  - [ ] Coverage: `pytest --cov=github` (≥85%)
- [ ] **CLI Interface**: All commands work
  - [ ] `github --version`
  - [ ] `github --help`
  - [ ] `github health`
- [ ] **REST API Interface**: All endpoints work
  - [ ] Health endpoint: `GET /health`
  - [ ] API documentation: `GET /docs`
  - [ ] Capability endpoints functional








### L3: Active (Best Practices)
- [ ] **Architecture Validation**:
  - [ ] Core/interface separation verified (0 circular dependencies)
  - [ ] Dependency injection pattern followed
  - [ ] All interfaces implement AbstractInterface
- [ ] **Docker Deployment**:
  - [ ] Docker image builds: `docker build -t github .`
  - [ ] Image size reasonable (<300MB)
  - [ ] Container runs: `docker run -p 8000:8000 github`
  - [ ] Health check passes in container
- [ ] **Documentation Complete**:
  - [ ] README.md updated with project specifics
  - [ ] API documentation generated
  - [ ] Architecture diagrams present
  - [ ] User guides updated

### L4: Deep (Optimization)
- [ ] **User Simulation** (<15 minutes):
  - [ ] New developer can set up in <5 min
  - [ ] Can execute basic workflow in <10 min
  - [ ] Documentation is clear and complete
- [ ] **Performance Metrics**:
  - [ ] Docker build: <180s
  - [ ] Test execution: <30s
  - [ ] Coverage: ≥85%
  - [ ] Image size: <300MB
  - [ ] API startup: <3s
  - [ ] Response time: <100ms (health endpoint)




---

## Verification Commands

### Setup
```bash
# Clone the repository (if verification in separate repo)
git clone https://github.com/liminalcommons/github.git
cd github

# Install dependencies
python -m pip install --upgrade pip
pip install -e ".[dev]"

```

### L1: Basic Verification
```bash
# File count
FILE_COUNT=$(find . -type f | wc -l)
echo "📁 Files generated: $FILE_COUNT (expected: ~80)"

# Core layer
test -d github/core && echo "✅ Core directory" || echo "❌ Core missing"
test -f github/core/models.py && echo "✅ Core models" || echo "❌ Models missing"
test -f github/core/service.py && echo "✅ Core service" || echo "❌ Service missing"

# Interface layers
test -d github/interfaces/cli && echo "✅ CLI interface" || echo "❌ CLI missing"
test -d github/interfaces/rest && echo "✅ REST interface" || echo "❌ REST missing"




# Dependencies
pip install -e ".[dev]" && echo "✅ Dependencies installed" || echo "❌ Install failed"
```

### L2: Quality Gates
```bash
# Ruff linting
ruff check . && echo "✅ Ruff lint passed" || echo "❌ Ruff lint failed"

# Ruff formatting
ruff format --check . && echo "✅ Ruff format passed" || echo "❌ Ruff format failed"

# Mypy type checking
mypy github && echo "✅ Mypy passed" || echo "❌ Mypy failed"

# Pytest tests
pytest && echo "✅ Tests passed" || echo "❌ Tests failed"

# Coverage
pytest --cov=github --cov-report=term-missing && echo "✅ Coverage ≥85%" || echo "❌ Coverage <85%"
```

### L2: Interface Testing
```bash
# CLI Interface
github --version && echo "✅ CLI version" || echo "❌ CLI version failed"
github health && echo "✅ CLI health" || echo "❌ CLI health failed"

# REST API Interface (start in background)
uvicorn github.interfaces.rest.app:app --host 0.0.0.0 --port 8000 &
API_PID=$!
sleep 3

# Test health endpoint
curl -f http://localhost:8000/health && echo "✅ REST health" || echo "❌ REST health failed"

# Test API docs
curl -f http://localhost:8000/docs && echo "✅ REST docs" || echo "❌ REST docs failed"

# Cleanup
kill $API_PID

```



### L3: Docker Deployment
```bash
# Build Docker image
docker build -t github:test . && echo "✅ Docker build" || echo "❌ Docker build failed"

# Check image size
IMAGE_SIZE=$(docker images github:test --format "{{.Size}}")
echo "📦 Image size: $IMAGE_SIZE (target: <300MB)"

# Run container
docker run -d --name github-test -p 8000:8000 github:test
sleep 5

# Test health in container
curl -f http://localhost:8000/health && echo "✅ Container health" || echo "❌ Container health failed"

# Cleanup
docker stop github-test
docker rm github-test
```

### L4: Performance Metrics
```bash
# Docker build time
time docker build -t github:perf . | tee build.log
BUILD_TIME=$(grep "real" build.log | awk '{print $2}')
echo "🚀 Docker build: $BUILD_TIME (target: <180s)"

# Test execution time
time pytest > test.log
TEST_TIME=$(grep "real" test.log | awk '{print $2}')
echo "🧪 Test execution: $TEST_TIME (target: <30s)"

# Coverage
pytest --cov=github --cov-report=term | grep "TOTAL"
echo "📊 Coverage (target: ≥85%)"

# API startup time
time uvicorn github.interfaces.rest.app:app --host 0.0.0.0 --port 8000 &
API_PID=$!
STARTUP_TIME=$(ps -p $API_PID -o etime= | awk '{print $1}')
echo "⚡ API startup: $STARTUP_TIME (target: <3s)"
kill $API_PID

# Response time (health endpoint)
curl -w "@curl-format.txt" -o /dev/null -s http://localhost:8000/health
echo "⏱️ Response time (target: <100ms)"
```

---

## Comprehensive Verification Plan

**Full Plan**: See [PLAN-2025-11-12-SAP-047-PHASE-6-L4-VERIFICATION.md](https://github.com/liminalcommons/chora-base/blob/main/docs/project-docs/plans/PLAN-2025-11-12-SAP-047-PHASE-6-L4-VERIFICATION.md) in chora-base repository.

**Day 15 (L1)**: Basic generation verification
**Day 16 (L2)**: Interface testing + quality gates
**Day 17 (L3)**: Architecture validation + Docker deployment
**Day 18 (L4)**: User simulation + performance metrics

---

## Claude Code Instructions

**If you are Claude Code verifying this project**, follow these steps:

### Step 1: Read Context
1. Read this file (VERIFICATION.md) for verification workflow
2. Read [CLAUDE.md](CLAUDE.md) for project navigation
3. Read [README.md](README.md) for project overview

### Step 2: Execute L1 Verification
1. Run the L1 verification commands above
2. Document results in `.chora/verification/l1-report.md`
3. Mark L1 checklist items as complete

### Step 3: Execute L2 Verification
1. Run quality gate commands
2. Test all interfaces (CLI, REST)

4. Document results in `.chora/verification/l2-report.md`
5. Mark L2 checklist items as complete

### Step 4: Execute L3 Verification
1. Validate architecture (core/interface separation)
2. Build and test Docker image
3. Document results in `.chora/verification/l3-report.md`
4. Mark L3 checklist items as complete

### Step 5: Execute L4 Verification
1. Run user simulation (time yourself)
2. Collect performance metrics

4. Document results in `.chora/verification/l4-report.md`
5. Mark L4 checklist items as complete

### Step 6: GO/NO-GO Decision
**Criteria for GO**:
- All L1-L4 checklist items complete
- All quality gates pass
- All interfaces functional
- Performance metrics meet targets
- Documentation complete

**If GO**: Proceed to GitHub template repository setup and production release.

**If NO-GO**: Document blockers, create issues in chora-base, iterate.

---

## Report Templates

### L1 Report Template
```markdown
# L1 Verification Report: GitHub

**Date**: [YYYY-MM-DD]
**Verified by**: [Claude Code / Human]
**Duration**: [X] minutes

## File Generation
- Total files: [X] (expected: ~80)
- Core layer: ✅/❌
- Interface layers: ✅/❌

## Dependencies
- Installation: ✅/❌
- No errors: ✅/❌

## L1 Result
- [ ] PASS - All L1 criteria met
- [ ] FAIL - Blockers: [list blockers]
```

### L2 Report Template
```markdown
# L2 Verification Report: GitHub

**Date**: [YYYY-MM-DD]
**Verified by**: [Claude Code / Human]
**Duration**: [X] minutes

## Quality Gates
- Ruff lint: ✅/❌
- Ruff format: ✅/❌
- Mypy: ✅/❌
- Pytest: ✅/❌ ([X] passed, [X] failed)
- Coverage: ✅/❌ ([X]%)

## Interface Testing
- CLI: ✅/❌
- REST API: ✅/❌

## L2 Result
- [ ] PASS - All L2 criteria met
- [ ] FAIL - Blockers: [list blockers]
```

### L3 Report Template
```markdown
# L3 Verification Report: GitHub

**Date**: [YYYY-MM-DD]
**Verified by**: [Claude Code / Human]
**Duration**: [X] minutes

## Architecture Validation
- Core/interface separation: ✅/❌
- Dependency injection: ✅/❌
- Circular dependencies: ✅/❌ (0 found)

## Docker Deployment
- Build success: ✅/❌
- Build time: [X]s (target: <180s)
- Image size: [X]MB (target: <300MB)
- Container runs: ✅/❌
- Health check: ✅/❌

## Documentation
- README.md: ✅/❌
- API docs: ✅/❌
- Architecture diagrams: ✅/❌

## L3 Result
- [ ] PASS - All L3 criteria met
- [ ] FAIL - Blockers: [list blockers]
```

### L4 Report Template
```markdown
# L4 Verification Report: GitHub

**Date**: [YYYY-MM-DD]
**Verified by**: [Claude Code / Human]
**Duration**: [X] minutes

## User Simulation
- Setup time: [X] min (target: <5 min)
- Workflow time: [X] min (target: <10 min)
- Total: [X] min (target: <15 min)

## Performance Metrics
| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Docker build | <180s | [X]s | ✅/❌ |
| Test execution | <30s | [X]s | ✅/❌ |
| Coverage | ≥85% | [X]% | ✅/❌ |
| Image size | <300MB | [X]MB | ✅/❌ |
| API startup | <3s | [X]s | ✅/❌ |
| Response time | <100ms | [X]ms | ✅/❌ |

## L4 Result
- [ ] PASS - All L4 criteria met
- [ ] FAIL - Blockers: [list blockers]
```

---

## Success Criteria Summary

**GO Decision**: All criteria met
**NO-GO Decision**: Any criterion fails

| Level | Criterion | Status |
|-------|-----------|--------|
| L1 | ~80 files generated | ⬜ |
| L1 | All layers present | ⬜ |
| L1 | Dependencies install | ⬜ |
| L2 | Quality gates pass | ⬜ |
| L2 | All interfaces work | ⬜ |
| L2 | Coverage ≥85% | ⬜ |
| L3 | Architecture valid | ⬜ |
| L3 | Docker deploys | ⬜ |
| L3 | Documentation complete | ⬜ |
| L4 | User simulation <15 min | ⬜ |
| L4 | Performance targets met | ⬜ |
| L4 | Advanced patterns work | ⬜ |

---

## Related Documentation

- **Comprehensive Plan**: [PLAN-2025-11-12-SAP-047-PHASE-6-L4-VERIFICATION.md](https://github.com/liminalcommons/chora-base/blob/main/docs/project-docs/plans/PLAN-2025-11-12-SAP-047-PHASE-6-L4-VERIFICATION.md)
- **chora-base Repository**: [https://github.com/liminalcommons/chora-base](https://github.com/liminalcommons/chora-base)
- **SAP-047 Documentation**: [docs/skilled-awareness/capability-server-template/](https://github.com/liminalcommons/chora-base/tree/main/docs/skilled-awareness/capability-server-template)
- **Generator Script**: [scripts/create-capability-server.py](https://github.com/liminalcommons/chora-base/blob/main/scripts/create-capability-server.py)

---

## Feedback and Issues

**Found issues during verification?**
1. Document in `.chora/verification/issues.md`
2. Create GitHub issue in chora-base: [https://github.com/liminalcommons/chora-base/issues](https://github.com/liminalcommons/chora-base/issues)
3. Tag with `SAP-047` and `verification`

**Questions or improvements?**
- Open discussion in chora-base repository
- Reference this verification run

---

**Generated by**: chora-base 5.0.0 SAP-047 Capability Server Template
**Last Updated**: {{ timestamp }}
