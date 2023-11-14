function BulletList(bulletlist)
  for _, item in ipairs(bulletlist.content) do
    if item.tag == "BulletList" then
      -- Add space after bullet point
      table.insert(item.content, 1, pandoc.RawBlock('markdown', ' '))
    end
  end
  return bulletlist
end
