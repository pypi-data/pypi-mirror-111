export function generateTagsRoute(_a) {
    var orgSlug = _a.orgSlug;
    return "/organizations/" + orgSlug + "/performance/summary/tags/";
}
export function tagsRouteWithQuery(_a) {
    var orgSlug = _a.orgSlug, transaction = _a.transaction, projectID = _a.projectID, query = _a.query;
    var pathname = generateTagsRoute({
        orgSlug: orgSlug,
    });
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