const std = @import("std");
const http = @import("zhp");
const os = std.os;

pub const Server = struct {
    app: http.Application,

    pub fn init(allocator: std.mem.Allocator) Server {
        return Server{ .app = http.Application.init(allocator, .{}) };
    }

    pub fn run(self: *Server) void {
        self.runErr() catch |err| {
            std.log.err("running http server: {}", .{err});
        };
    }

    fn runErr(self: *Server) !void {
        try self.app.listen("0.0.0.0", 80);
        try self.app.start();
    }
};

pub const middleware = [_]http.Middleware{http.Middleware.create(http.middleware.LoggingMiddleware)};

pub const routes = [_]http.Route{
    http.Route.create("/", IndexHandler),
    http.Route.create("/metrics", MetricsHandler),
};

const IndexHandler = struct {
    const template = @embedFile("../static/index.html");

    pub fn get(_: *IndexHandler, _: *http.Request, response: *http.Response) !void {
        _ = try response.stream.write(template);
    }
};

const MetricsHandler = struct {
    pub fn get(_: *MetricsHandler, _: *http.Request, response: *http.Response) !void {
        const flag = os.getenv("FLAG") orelse "fakeflag";

        try response.headers.put("Content-Type", "text/plain; version=0.0.4");
        try response.stream.print(
            \\app{{flag="{s}"}} 1
            \\
        , .{flag});
    }
};
