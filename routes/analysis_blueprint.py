from flask import Blueprint, request, jsonify

from algorithms import download_and_extract_tex
from exts import llm, jinja_env, mongo

analysis_blueprint = Blueprint("analysis_blueprint", __name__)


@analysis_blueprint.route("/analysis", methods=["POST"])
def analyze_paper():
    arxiv_id = request.json.get("arxiv_id")
    section = request.json.get("section")

    if not arxiv_id:
        return jsonify({"error": "arxiv_id is required"}), 400
    if section not in ["full", "intro", "method", "experiments"]:
        return jsonify({"error": "Invalid section specified"}), 400

    content = mongo.db.paper_content.find_one({"arxiv_id": arxiv_id})
    if not content:
        try:
            content_section = download_and_extract_tex(arxiv_id)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        content = {
            "arxiv_id": arxiv_id,
            "section": content_section,
        }
        mongo.db.paper_content.insert_one(content)

    section_name = section if section != "intro" else "introduction"
    if "analysis" not in content or section_name not in content["analysis"]:
        prompt = jinja_env.get_template(f"{section}_analysis.j2").render(
            document=content["section"][section_name]
        )
        response = llm["client"].chat.completions.create(
            messages=[{"role": "user", "content": prompt}], **llm["config"]
        )
        analysis = response.choices[0].message.content
        mongo.db.paper_content.update_one(
            {"arxiv_id": arxiv_id}, {"$set": {f"analysis.{section_name}": analysis}}
        )
    else:
        analysis = content["analysis"][section_name]

    return jsonify({"anaysis": analysis}), 200
