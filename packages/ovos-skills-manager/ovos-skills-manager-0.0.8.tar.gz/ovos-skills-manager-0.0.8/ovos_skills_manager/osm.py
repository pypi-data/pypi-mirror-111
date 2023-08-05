from ovos_utils.log import LOG
from ovos_utils.json_helper import merge_dict
from json_database import JsonStorageXDG

from ovos_skills_manager import SkillEntry
from ovos_skills_manager.appstores.andlo import AndloSkillList
from ovos_skills_manager.appstores.mycroft_marketplace import \
    MycroftMarketplace
from ovos_skills_manager.appstores.pling import Pling
from ovos_skills_manager.appstores.ovos import OVOSstore
from ovos_skills_manager.appstores.neon import NeonSkills
from ovos_skills_manager.exceptions import UnknownAppstore
from ovos_skills_manager.appstores.local import InstalledSkills, get_skills_folder
from ovos_skills_manager.github import author_repo_from_github_url


def safe_get_skills_folder():
    try:
        return get_skills_folder()
    except:
        return ""


class OVOSSkillsManager:
    def __init__(self):
        self.config = JsonStorageXDG("OVOS-SkillsManager")
        default_config = {
            "local": {
                "active": True,
                "url": safe_get_skills_folder(),
                "parse_github": False,
                "priority": 1},
            "ovos": {
                "active": True,
                "url": "https://github.com/OpenVoiceOS/OVOS-appstore",
                "parse_github": False,
                "priority": 2},
            "mycroft_marketplace": {
                "active": False,
                "url": "https://market.mycroft.ai/",
                "parse_github": False,
                "priority": 5},
            "pling": {
                "active": False,
                "url": "https://apps.plasma-bigscreen.org/",
                "parse_github": False,
                "priority": 10},
            "neon": {
                "active": False,
                "url": "https://github.com/NeonGeckoCom/neon-skills-submodules/",
                "parse_github": False,
                "auth_token": None,
                "priority": 50},
            "andlo_skill_list": {
                "active": False,
                "url": "https://andlo.gitbook.io/mycroft-skills-list/",
                "parse_github": False,
                "priority": 100}
        }

        if "appstores" not in self.config:
            # NOTE, below should match Appstore.appstore_id
            self.config["appstores"] = default_config
            self.save_config()
        self.config["appstores"] = merge_dict(self.config["appstores"],
                                              default_config,
                                              new_only=True,
                                              no_dupes=True)
        self._boostrap_tracker = {}
        self.save_config()
        self._threads = []

    def get_active_appstores(self, bootstrap=False):
        stores = {}
        for appstore_id in self.config["appstores"]:
            if self.config["appstores"][appstore_id]["active"]:
                if bootstrap and appstore_id not in self._boostrap_tracker:
                    self._boostrap_tracker[appstore_id] = True
                elif bootstrap and appstore_id in self._boostrap_tracker:
                    bootstrap = False
                stores[appstore_id] = self.get_appstore(appstore_id,
                                                        bootstrap=bootstrap)
        return stores

    def get_appstore(self, appstore_id, bootstrap=True):
        if self.config["appstores"][appstore_id]["active"]:
            parse_github = self.config["appstores"][appstore_id]["parse_github"]
            store = self.name_to_appstore(appstore_id)
            if bootstrap and appstore_id not in self._boostrap_tracker:
                self._boostrap_tracker[appstore_id] = True
            elif bootstrap and appstore_id in self._boostrap_tracker:
                bootstrap = False
            return store(parse_github=parse_github, bootstrap=bootstrap)
        return None

    @staticmethod
    def name_to_appstore(name):
        if name in ["pling", "bigscreen"]:
            return Pling
        elif name in ["mycroft", "mycroft_marketplace"]:
            return MycroftMarketplace
        elif name in ["andlo", "andlo_skill_list"]:
            return AndloSkillList
        elif name in ["ovos", "ovos_appstore", "ovos_marketplace"]:
            return OVOSstore
        elif name in ["neon", "neon_gecko", "neon_skills"]:
            return NeonSkills
        elif name in ["local", "local_skills", "installed",
                      "installed_skills"]:
            return InstalledSkills
        else:
            raise UnknownAppstore

    def save_config(self):
        self.config.store()

    def clear_cache(self, appstore_id=None):
        if appstore_id:
            self.get_appstore(appstore_id).clear_cache()
        else:
            for appstore in self.appstores:
                appstore.clear_cache()

    def validate_appstore_name(self, appstore):
        if appstore in ["pling", "bigscreen"]:
            appstore = "pling"
        elif appstore in ["mycroft", "mycroft_marketplace"]:
            appstore = "mycroft_marketplace"
        elif appstore in ["andlo", "andlo_skill_list"]:
            appstore = "andlo_skill_list"
        elif appstore in ["ovos", "ovos_appstore", "ovos_marketplace"]:
            appstore = "ovos"
        elif appstore in ["neon", "neon_gecko", "neon_skills"]:
            appstore = "neon"
        elif appstore in ["local", "local_skills", "installed",
                          "installed_skills"]:
            appstore = "local"
        elif appstore not in self.config["appstores"]:
            raise UnknownAppstore
        return appstore

    def enable_appstore(self, appstore_id):
        appstore_id = self.validate_appstore_name(appstore_id)
        self.config["appstores"][appstore_id]["active"] = True

    def set_appstore_priority(self, appstore_id, priority):
        appstore_id = self.validate_appstore_name(appstore_id)
        self.config["appstores"][appstore_id]["priority"] = priority

    def set_appstore_auth_token(self, appstore_id, token):
        appstore_id = self.validate_appstore_name(appstore_id)
        self.config["appstores"][appstore_id]["auth_token"] = token

    def disable_appstore(self, appstore_id):
        appstore_id = self.validate_appstore_name(appstore_id)
        self.config["appstores"][appstore_id]["active"] = False

    def sync_appstores(self, merge=False, new_only=False, threaded=False):
        stores = self.get_active_appstores()
        for appstore_id in stores:
            LOG.info("Syncing skills from " + appstore_id)
            store = stores[appstore_id]
            store.authenticate()
            if threaded:
                # TODO this will cause auth issues
                t = store.sync_skills_list_threaded(merge, new_only)
                self._threads.append(t)
            else:
                store.sync_skills_list(merge, new_only)
                store.clear_authentication()

    @property
    def total_skills(self):
        return sum([s.total_skills() for s in self.appstores])

    @property
    def appstores(self):
        stores = []
        for appstore_id in self.config["appstores"]:
            store = self.get_appstore(appstore_id)
            if not store:
                continue
            priority = self.config["appstores"][appstore_id]["priority"]
            stores.append((store, priority))
        return [s[0] for s in sorted(stores, key=lambda k: k[1])]

    def search_skills(self, name, as_json=False, fuzzy=True, thresh=0.85,
                      ignore_case=True):
        for store in self.appstores:
            store.authenticate()
            for skill in store.search_skills(name, as_json, fuzzy,  thresh,
                                             ignore_case):
                yield skill
            store.clear_authentication()

    def search_skills_by_id(self, skill_id, as_json=False, fuzzy=False,
                            thresh=0.85, ignore_case=True):
        """ skill_id is repo.author , case insensitive,
        searchs by name and filters results by author """
        for store in self.appstores:
            store.authenticate()
            for skill in store.search_skills_by_id(skill_id, as_json,
                                                   fuzzy=fuzzy,
                                                   ignore_case=ignore_case,
                                                   thresh=thresh):
                yield skill
            store.clear_authentication()

    def search_skills_by_name(self, name, as_json=False,
                              fuzzy=True, thresh=0.85, ignore_case=True):
        for store in self.appstores:
            store.authenticate()
            for skill in store.search_skills_by_name(name, as_json, fuzzy,
                                                     thresh, ignore_case):
                yield skill
            store.clear_authentication()

    def search_skills_by_url(self, url, as_json=False):
        for store in self.appstores:
            store.authenticate()
            for skill in store.search_skills_by_url(url, as_json):
                store.clear_authentication()
                return [skill]
        LOG.warning(f"No results found for: {url}")
        return []

    def search_skills_by_category(self, category, as_json=False,
                                  fuzzy=True, thresh=0.85, ignore_case=True):
        for store in self.appstores:
            store.authenticate()
            for skill in store.search_skills_by_category(category, as_json,
                                                         fuzzy, thresh,
                                                         ignore_case):
                yield skill
            store.clear_authentication()

    def search_skills_by_author(self, authorname, as_json=False,
                                fuzzy=True, thresh=0.85, ignore_case=True):
        for store in self.appstores:
            store.authenticate()
            for skill in store.search_skills_by_author(authorname, as_json,
                                                       fuzzy, thresh,
                                                       ignore_case):
                yield skill
            store.clear_authentication()

    def search_skills_by_tag(self, tag, as_json=False,
                             fuzzy=True, thresh=0.85, ignore_case=True):
        for store in self.appstores:
            store.authenticate()
            for skill in store.search_skills_by_tag(tag, as_json, fuzzy,
                                                    thresh, ignore_case):
                yield skill
            store.clear_authentication()

    def search_skills_by_description(self, value, as_json=False,
                                     fuzzy=True, thresh=0.85,
                                     ignore_case=True):
        for store in self.appstores:
            store.authenticate()
            for skill in store.search_skills_by_description(value, as_json,
                                                            fuzzy, thresh,
                                                            ignore_case):
                yield skill
            store.clear_authentication()

    @staticmethod
    def skill_entry_from_url(url: str):
        """
        Builds a minimal SkillEntry object from the passed GitHub URL to use for skill installation
        :param url: URL of skill to install
        :return: SkillEntry object with url, branch, requirements, and authorname populated
        """
        from ovos_skills_manager.exceptions import GithubInvalidBranch, GithubFileNotFound
        from ovos_skills_manager.github import get_branch_from_github_url, normalize_github_url, get_requirements_json,\
            get_skill_json
        from ovos_skills_manager.skill_entry import SkillEntry
        try:
            branch = get_branch_from_github_url(url)
        except GithubInvalidBranch:
            branch = None
        url = normalize_github_url(url)
        requirements = get_requirements_json(url, branch)
        requirements["system"] = {k: v.split() for k, v in requirements.get("system", {}).items()}
        try:
            json = get_skill_json(url, branch)
            requirements = merge_dict(requirements, json.get("requirements", {}),
                                      merge_lists=True, skip_empty=True, no_dupes=True)
        except GithubFileNotFound:
            json = {"authorname": author_repo_from_github_url(url)[0]}
        return SkillEntry.from_json({"url": url,
                                     "branch": branch,
                                     "requirements": requirements,
                                     "authorname": json.get("authorname")}, False)

    def install_skill_from_url(self, url: str, skill_dir: str = None):
        """
        Installs a Skill from the passed url
        :param url: Git url of skill to install (including optional branch spec)
        :param skill_dir: Skills directory to install to (skill unpacked to {folder}/{skill.uuid})
        """
        self.install_skill(self.skill_entry_from_url(url), skill_dir)

    def install_skill(self, skill: SkillEntry, folder=None):
        """
        Installs a SkillEntry with any required auth_token
        :param skill: Skill to install
        :param folder: Skills directory to install to (skill unpacked to {folder}/{skill.uuid})
        """
        store = None
        try:
            self.validate_appstore_name(skill.appstore)
            store = self.get_appstore(skill.appstore)
            store.authenticate(bootstrap=False)
        except:
            pass
        skill.install(folder)
        if store:
            store.clear_authentication()

    def __iter__(self):
        for store in self.appstores:
            for skill in store:
                yield skill
