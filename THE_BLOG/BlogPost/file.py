class PostView:
    def get_queryset(self):
        self.author_slug_name ="slugs"
        self.category = "lifestyle"
        return self.author_slug_name
    def vis(self):
        return self.get_queryset().category    

Post=PostView()
print(Post.vis())