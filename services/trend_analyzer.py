class TrendAnalyzer:

    def analyse(self, history):

        if len(history) < 3:

            return {
                "trend": "Insufficient history",
                "prediction": "Collecting data"
            }

        risks = []

        for item in history[-5:]:

            analysis = item.get("analysis", {})

            risks.append(
                analysis.get("risk_score", 0)
            )

        if risks[-1] > risks[0]:

            return {

                "trend": "Vehicle risk increasing",

                "prediction": "Failure probability rising"

            }

        elif risks[-1] < risks[0]:

            return {

                "trend": "Vehicle condition improving",

                "prediction": "Risk reducing"

            }

        return {

            "trend": "Stable",

            "prediction": "No significant change"

        }


trend_analyzer = TrendAnalyzer()