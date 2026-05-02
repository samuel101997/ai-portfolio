# app.py - Streamlit interface for the NovaTel Automation Workflow
# Classify customer messages, route to actions, view logs

import json
import streamlit as st
from workflow.router import process_message
from workflow.logger import load_logs, clear_logs
from config import SAMPLE_MESSAGES_PATH

st.set_page_config(page_title="NovaTel Workflow Automation", page_icon="⚡")
st.title("⚡ NovaTel Workflow Automation")
st.caption("Classify customer messages, auto-route to actions, and track everything.")

# --- Sidebar: Mode Selection ---
with st.sidebar:
    st.header("Mode")
    mode = st.radio("Choose mode:", ["Single Message", "Batch Process", "View Logs"])

    if st.button("🗑️ Clear Logs"):
        clear_logs()
        st.success("Logs cleared.")

# --- Mode 1: Single Message ---
if mode == "Single Message":
    st.markdown("### Process a Customer Message")

    customer_name = st.text_input("Customer Name:", placeholder="e.g., Sarah Chen")
    message = st.text_area("Customer Message:", height=120,
        placeholder="e.g., I was charged $45 for a data add-on I never purchased...")

    if st.button("🚀 Process Message", type="primary"):
        if not customer_name or not message:
            st.warning("Enter both a name and a message.")
        else:
            with st.spinner("Classifying and routing..."):
                result = process_message(customer_name, message)

            # Display classification
            cls = result["classification"]
            col1, col2, col3 = st.columns(3)
            col1.metric("Intent", cls["intent"])
            col2.metric("Priority", cls["priority"])
            col3.metric("Confidence", f"{cls.get('confidence', 0):.0%}")

            st.markdown(f"**Summary:** {cls['summary']}")

            if cls.get("key_entities"):
                st.markdown(f"**Key Entities:** {', '.join(cls['key_entities'])}")

            # Display actions taken
            st.markdown("### Actions Taken")
            for action in result["actions_taken"]:
                action_labels = {
                    "create_ticket": "📋 Support ticket created",
                    "draft_reply": "✉️ Auto-reply drafted",
                    "escalate": "🔴 Flagged for escalation (high priority)",
                    "flag_retention": "🟡 Flagged for retention team",
                    "escalate_manager": "🚨 Escalated to manager",
                    "flag_billing_review": "💰 Flagged for billing review",
                }
                st.markdown(f"- {action_labels.get(action, action)}")

            # Display ticket
            with st.expander("📋 View Support Ticket"):
                st.json(result["ticket"])

            # Display draft reply
            with st.expander("✉️ View Draft Reply"):
                st.write(result["draft_reply"])

# --- Mode 2: Batch Process ---
elif mode == "Batch Process":
    st.markdown("### Batch Process Sample Messages")
    st.caption("Process all 22 sample NovaTel customer messages at once.")

    if st.button("⚡ Run Batch", type="primary"):
        with open(SAMPLE_MESSAGES_PATH, "r") as f:
            messages = json.load(f)

        progress = st.progress(0)
        status = st.empty()
        results = []

        for i, msg in enumerate(messages):
            status.text(f"Processing {i+1}/{len(messages)}: {msg['customer']}...")
            result = process_message(msg["customer"], msg["message"])
            results.append(result)
            progress.progress((i + 1) / len(messages))

        status.text(f"✅ Processed {len(messages)} messages!")

        # Summary table
        st.markdown("### Results Summary")
        summary_data = []
        for r in results:
            cls = r["classification"]
            summary_data.append({
                "Customer": r["customer"],
                "Intent": cls["intent"],
                "Priority": cls["priority"],
                "Confidence": f"{cls.get('confidence', 0):.0%}",
                "Actions": ", ".join(r["actions_taken"]),
            })
        st.dataframe(summary_data, use_container_width=True)

        # Stats
        st.markdown("### Classification Stats")
        intents = [r["classification"]["intent"] for r in results]
        priorities = [r["classification"]["priority"] for r in results]

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**By Intent:**")
            for intent in set(intents):
                count = intents.count(intent)
                st.markdown(f"- {intent}: {count}")
        with col2:
            st.markdown("**By Priority:**")
            for priority in set(priorities):
                count = priorities.count(priority)
                st.markdown(f"- {priority}: {count}")

# --- Mode 3: View Logs ---
elif mode == "View Logs":
    st.markdown("### Execution Logs")
    logs = load_logs()

    if not logs:
        st.info("No logs yet. Process some messages first.")
    else:
        st.markdown(f"**Total logged entries:** {len(logs)}")

        for log in reversed(logs):
            cls = log.get("classification", {})
            with st.expander(
                f"#{log.get('log_id')} | {log.get('customer')} | "
                f"{cls.get('intent')} | {cls.get('priority')} | "
                f"{log.get('timestamp', 'N/A')[:19]}"
            ):
                st.json(log)