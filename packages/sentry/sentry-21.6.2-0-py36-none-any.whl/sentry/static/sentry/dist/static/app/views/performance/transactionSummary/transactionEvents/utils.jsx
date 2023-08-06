export function eventsRouteWithQuery(_a) {
    var orgSlug = _a.orgSlug, transaction = _a.transaction, projectID = _a.projectID, query = _a.query;
    var pathname = "/organizations/" + orgSlug + "/performance/summary/events/";
    return {
        pathname: pathname,
        query: {
            transaction: transaction,
            project: projectID,
            environment: query.environment,
            statsPeriod: query.statsPeriod,
            start: query.start,
            end: query.end,
            query: query.query,
        },
    };
}
//# sourceMappingURL=utils.jsx.map