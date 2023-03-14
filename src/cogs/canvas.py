import requests
import os
from discord.ext import commands
from datetime import datetime


class Canvas(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.canvas_token = os.environ["CANVAS_TOKEN"]

    def perform_request(self, endpoint):
        print(f"GET https://canvas.instructure.com/api/v1/{endpoint}")
        return requests.get(
            f"https://canvas.instructure.com/api/v1/{endpoint}",
            headers={"Authorization": f"Bearer {self.canvas_token}"},
        ).json()

    @commands.command(description="Fetches and displays information about user from the Canvas API")
    async def canvasfind(self, ctx, *, query):
        found_students = self.perform_request(f"search/recipients?search={query}")

        if not found_students:
            await ctx.message.edit(content="Not found")
        else:
            found_student = found_students[0]  # select first student

            courses = self.perform_request("courses")
            try:
                join_date = datetime.strptime(
                    self.perform_request(
                        f"courses/{list(found_student['common_courses'].keys())[0]}/users/{found_student['id']}"
                    )["created_at"],
                    "%Y-%m-%dT%H:%M:%S%z",
                )
            except:
                join_date = datetime.now()

            common_courses = found_student["common_courses"].keys()

            await ctx.message.edit(
                content=f"""
**{found_student['full_name']}** - {found_student['id']}

**Known Courses:**
{", ".join([course["name"] for course in courses if str(
    course["id"]) in common_courses])}

**Join Date:**
<t:{int(join_date.timestamp())}:R>

**Canvas avatar:**
{found_student["avatar_url"]}"""
            )

    @commands.command(description="Searches Canvas addressbook by name")
    async def canvassearch(self, ctx, *, name):
        found_students = self.perform_request(
            f"search/recipients?search={name}&per_page=100",
        )
        await ctx.message.edit(
            content=", ".join([student["name"] for student in found_students])
        )

    @commands.command(description="Fetches TODO assignments from the Canvas API")
    async def todo(self, ctx):
        courses = {}
        todo_assignments = self.perform_request("users/self/todo?per_page=100")

        for assignment in todo_assignments:
            if assignment["course_id"] in courses:
                courses[assignment["course_id"]].append(assignment)
            else:
                courses[assignment["course_id"]] = [assignment]

        content = f"{len(todo_assignments)} assignments remaining.\n"
        for course in courses:
            content += f"\n**{courses[course][0]['context_name']}**:\n"
            for item in courses[course]:
                content += f'{item["assignment"]["name"]} due <t:{int(datetime.strptime(item["assignment"]["due_at"], "%Y-%m-%dT%H:%M:%SZ").timestamp())}:R>\n'

        await ctx.message.edit(content=content)


def setup(client):
    client.add_cog(Canvas(client))
