FROM nginx:1.28.0-alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY *.html *.css app.js metrics.js monitoring.js appearance.js prediction.js recommendations.js racks.js racks.json pmv2.js experiment.json aggregate.js energy.js friendly-errors.js help-content.js ui-kit.js dashboard-ui.js flows-logic.js flows.js /usr/share/nginx/html/
EXPOSE 3001
