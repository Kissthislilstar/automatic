import html
import json
import os

from modules import shared, ui_extra_networks, sd_models


class ExtraNetworksPageCheckpoints(ui_extra_networks.ExtraNetworksPage):
    def __init__(self):
        super().__init__('Checkpoints')

    def refresh(self):
        shared.refresh_checkpoints()

    def list_items(self):
        checkpoint: sd_models.CheckpointInfo
        for index, (name, checkpoint) in enumerate(sd_models.checkpoints_list.items()):
            path, ext = os.path.splitext(checkpoint.filename)
            yield {
                "name": checkpoint.name_for_extra,
                "filename": path,
                "preview": self.find_preview(path),
                "description": self.find_description(path),
                "search_term": self.search_terms_from_path(checkpoint.filename) + " " + (checkpoint.sha256 or ""),
                "onclick": '"' + html.escape(f"""return selectCheckpoint({json.dumps(name)})""") + '"',
                "local_preview": f"{path}.{shared.opts.samples_format}",
                "sort_keys": {'default': index, **self.get_sort_keys(checkpoint.filename)},

            }

    def allowed_directories_for_previews(self):
        return [v for v in [shared.opts.ckpt_dir, sd_models.model_path] if v is not None]
