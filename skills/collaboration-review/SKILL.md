---
name: Collaboration Review
description: This skill should be used when the user asks to "复盘", "总结经验", "记录错误", "踩坑了", "做错了", "下次避免", "协作复盘", "工作复盘", "反思", "记录教训", or wants to review and document mistakes, pitfalls, or lessons learned from a collaboration session. Use this skill to systematically analyze what went wrong, why it happened, and how to improve in the future.
version: 0.1.0
---

# Collaboration Review Skill

Systematically review and document mistakes, pitfalls, and lessons learned from collaboration sessions. The goal is to improve efficiency by avoiding repeated errors.

## When to Use This Skill

Use this skill when:
- User says "复盘" or "做复盘"
- User mentions something went wrong or suboptimal
- User expresses dissatisfaction or frustration
- After completing a significant task, user wants to reflect on the process
- User asks "下次怎么避免" or "怎么改进"
- User says "踩坑了" or "犯错了"

Do NOT use this skill when:
- User is just asking casual questions
- User wants quick information without deep analysis
- This is the first time working together (no history to review)

## Overview

This skill provides a structured approach to:

1. **Identify issues** - What went wrong or could be improved?
2. **Analyze root causes** - Why did it happen?
3. **Extract lessons** - What can we learn?
4. **Document for future** - Write it down to reference later
5. **Update guidelines** - Improve collaboration based on insights

## Workflow

### Step 1: Gather Context

Ask the user clarifying questions if needed:
- "你想复盘哪个具体的事情？"
- "有哪些地方你觉得不好的？"
- "这次协作中你最在意的问题是什么？"

### Step 2: Identify Issues

Work with user to identify:
- What went wrong?
- What was inefficient?
- What caused frustration?
- What could be done better?

Categories to consider:
- **Communication**: misunderstandings, lack of clarity, wrong assumptions
- **Technical**: tool failures, environment issues, setup problems
- **Process**: workflow inefficiencies, missing steps, wrong priorities
- **Expectations**: mismatched expectations, unclear goals

### Step 3: Analyze Root Causes

For each issue identified, ask:
- **What happened?** (fact)
- **Why did it happen?** (cause)
- **What was the impact?** (consequence)
- **Who was affected?** (stakeholder)

Use this framework:

```
Issue: [描述问题]
原因: [为什么会发生]
影响: [造成了什么后果]
改进: [下次怎么避免]
```

### Step 4: Extract Principles

From the analysis, extract general principles:

**For AI:**
- What should I do differently?
- What signals should I watch for?
- What questions should I ask?
- When should I stop and check?

**For Human:**
- What should you tell me directly?
- What signals should you give?
- What preferences should you communicate?

### Step 5: Document

Create a review document in the project's `COLLABORATION_REVIEW.md` or a dedicated review file.

Structure:
```markdown
# 协作复盘记录

## 日期
## 主题

## 做得好的地方 ✅

## 做得不好的地方 ❌

## 问题分析
### Issue 1
- 发生了什么
- 原因分析
- 改进方案

## 经验原则
### 给 AI 的建议
### 给人类的建议

## 下次改进
```

### Step 6: Commit to Git

Push the review document to the project's repository so it's preserved for future reference.

## Document Location

Store review documents in:
- Project root: `COLLABORATION_REVIEW.md`
- Or: `reviews/YYYY-MM-DD-topic.md`

## Examples

### Example 1: GitHub Authorization Issue

**Issue**: GitHub authorization kept failing, AI kept retrying without asking.

**Analysis**:
- AI tried same failed method multiple times
- Didn't ask user for alternative
- Didn't recognize user's frustration signals

**Principles**:
- After 1 failure, offer alternatives
- Ask "要不要换个方式？"
- Listen for frustration signals like "你来做"

### Example 2: Communication Mismatch

**Issue**: User said one thing, AI understood another.

**Analysis**:
- Ambiguous phrasing
- AI didn't confirm understanding
- Didn't ask clarifying questions early

**Principles**:
- Summarize understanding back to user
- Ask "你是说...吗？"
- Confirm before proceeding with assumptions

## Key Principles Summary

### AI Should Do
- Check in after failures: "要不要换个方式？"
- Ask before assuming: "我理解得对吗？"
- Set expectations: "这可能需要几分钟"
- Watch for frustration: user saying "算了" / "直接告诉我"
- Offer choices: "A. 继续尝试 B. 换个方式 C. 先停一下"

### Human Should Do
- Say "我不满意" or "我烦了" directly
- Say "停一停" to interrupt
- Give explicit preferences upfront
- Say "直接说步骤" when wanting quick answers

## Integration with Other Skills

This skill should be used proactively:
- After any significant error or issue
- When user expresses any level of frustration
- At project milestones for reflection
- When transitioning between major phases

## Additional Resources

### Reference Files
- **`references/root_cause_analysis.md`** - Detailed root cause analysis methods
- **`references/review_templates.md`** - Templates for different review types
- **`references/communication_signals.md`** - Signals to watch for in communication

### Scripts
- **`scripts/extract_issues.py`** - Tool to help extract issues from conversation
- **`scripts/generate_review.py`** - Generate review document from structured input
